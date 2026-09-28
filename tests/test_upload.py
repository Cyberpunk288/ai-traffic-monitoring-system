"""Run with the backend on port 8000: python -m unittest discover -s tests -v."""

import base64
import json
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import cv2
import numpy as np

BASE_URL = "http://127.0.0.1:8000"


def upload(filename, contents):
    boundary = "prototype-test-boundary"
    body = (
        f'--{boundary}\r\nContent-Disposition: form-data; name="file"; '
        f'filename="{filename}"\r\nContent-Type: application/octet-stream\r\n\r\n'
    ).encode() + contents + f"\r\n--{boundary}--\r\n".encode()
    request = Request(BASE_URL + "/api/process", data=body, headers={
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    })
    try:
        response = urlopen(request, timeout=60)
    except HTTPError as error:
        response = error
    with response:
        return response.status, json.load(response)


class UploadTests(unittest.TestCase):
    def test_health(self):
        with urlopen(BASE_URL + "/api/health", timeout=5) as response:
            self.assertEqual(json.load(response), {"status": "ok"})

    def test_png_dimensions_and_real_grayscale(self):
        # A pure red image should become grayscale intensity 76.
        image = np.zeros((40, 80, 3), dtype=np.uint8)
        image[:, :] = (0, 0, 255)
        _, encoded = cv2.imencode(".png", image)
        status, result = upload("vehicle.PNG", encoded.tobytes())
        self.assertEqual(status, 200)
        self.assertEqual((result["width"], result["height"]), (80, 40))
        self.assertEqual(result["format"], "PNG")
        grayscale = cv2.imdecode(np.frombuffer(base64.b64decode(
            result["grayscale_image"].split(",", 1)[1]), np.uint8), cv2.IMREAD_UNCHANGED)
        self.assertEqual(grayscale.shape, (40, 80))
        self.assertTrue(np.all(grayscale == 76))
        self.assertEqual(result["detection_count"], len(result["detections"]))
        annotated = cv2.imdecode(np.frombuffer(base64.b64decode(
            result["annotated_image"].split(",", 1)[1]), np.uint8), cv2.IMREAD_COLOR)
        self.assertEqual(annotated.shape, image.shape)
        self.assertNotIn("plate_text", result)

    def test_jpeg_and_resized_preview(self):
        _, encoded = cv2.imencode(".jpg", np.zeros((800, 1600, 3), np.uint8))
        status, result = upload("vehicle.jpeg", encoded.tobytes())
        self.assertEqual(status, 200)
        self.assertEqual((result["width"], result["height"]), (1600, 800))
        self.assertEqual(result["format"], "JPEG")
        preview = cv2.imdecode(np.frombuffer(base64.b64decode(
            result["grayscale_image"].split(",", 1)[1]), np.uint8), cv2.IMREAD_UNCHANGED)
        self.assertEqual(preview.shape, (600, 1200))

    def test_invalid_uploads(self):
        _, png = cv2.imencode(".png", np.zeros((10, 10, 3), np.uint8))
        cases = [
            ("notes.txt", b"text", 400),
            ("fake.jpg", b"not an image", 400),
            ("empty.png", b"", 400),
            ("wrong.jpg", png.tobytes(), 400),
            ("damaged.png", b"\x89PNG\r\n\x1a\ninvalid", 400),
            ("large.jpg", b"x" * (10 * 1024 * 1024 + 1), 413),
        ]
        for filename, contents, expected in cases:
            with self.subTest(filename=filename):
                status, result = upload(filename, contents)
                self.assertEqual(status, expected)
                self.assertIsInstance(result["detail"], str)

    def test_missing_file(self):
        request = Request(BASE_URL + "/api/process", data=b"", method="POST")
        with self.assertRaises(HTTPError) as context:
            urlopen(request, timeout=5)
        self.assertEqual(context.exception.code, 422)
        context.exception.close()


if __name__ == "__main__":
    unittest.main()
