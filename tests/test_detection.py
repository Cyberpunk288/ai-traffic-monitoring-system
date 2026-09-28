"""Deterministic detection tests; only inference output is mocked."""

import base64
from io import BytesIO
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import cv2
import numpy as np
from fastapi import HTTPException, UploadFile

from backend import main


def decode(url):
    assert url.startswith("data:image/png;base64,")
    return cv2.imdecode(np.frombuffer(base64.b64decode(url.split(",", 1)[1]),
                                     np.uint8), cv2.IMREAD_COLOR)


def box(coords, confidence=0.85):
    return SimpleNamespace(xyxy=np.array([coords]), conf=[confidence], cls=[0])


class DetectionTests(unittest.TestCase):
    def setUp(self):
        self.image = np.arange(80 * 120 * 3, dtype=np.uint8).reshape(80, 120, 3)
        _, encoded = cv2.imencode(".png", self.image)
        self.contents = encoded.tobytes()

    def upload(self):
        return UploadFile(filename="vehicle.png", file=BytesIO(self.contents))

    def process(self, boxes):
        result = SimpleNamespace(boxes=boxes, names={0: "license_plate"})
        upload = self.upload()
        with patch.object(main.model, "predict", return_value=[result]) as predict:
            response = main.process_image(upload)
        self.assertTrue(upload.file.closed)
        self.assertEqual(predict.call_count, 1)
        np.testing.assert_array_equal(predict.call_args.kwargs["source"], self.image)
        self.assertEqual(predict.call_args.kwargs["conf"], 0.25)
        self.assertFalse(predict.call_args.kwargs["save"])
        self.assertEqual(response["size_bytes"], len(self.contents))
        self.assertNotIn("plate_text", response)
        return response

    def test_zero_detections(self):
        response = self.process([])
        self.assertEqual(response["detections"], [])
        self.assertEqual(response["detection_count"], 0)
        np.testing.assert_array_equal(decode(response["annotated_image"]), self.image)

    def test_one_and_multiple_plates(self):
        for count in (1, 2):
            with self.subTest(count=count):
                boxes = [box([10, 20, 50, 40]), box([60, 45, 110, 70], 0.67)][:count]
                response = self.process(boxes)
                self.assertEqual(response["detection_count"], count)
                self.assertEqual(len(response["detections"]), count)
                for detection, expected in zip(response["detections"], boxes):
                    x1, y1, x2, y2 = expected.xyxy[0]
                    self.assertEqual(detection["class_name"], "license_plate")
                    self.assertAlmostEqual(detection["confidence"], expected.conf[0])
                    self.assertEqual(detection["bbox"], dict(x1=x1, y1=y1, x2=x2, y2=y2))
                    np.testing.assert_array_equal(decode(detection["cropped_image"]),
                                                  self.image[y1:y2, x1:x2])
                    self.assertNotIn("plate_text", detection)
                annotated = decode(response["annotated_image"])
                self.assertEqual(annotated.shape, self.image.shape)
                np.testing.assert_array_equal(annotated[20, 10], [0, 255, 0])
                self.assertFalse(np.array_equal(annotated, self.image))

    def test_clipped_fractional_and_empty_boxes(self):
        response = self.process([box([-2.5, 20.2, 130.5, 90]), box([120, 0, 130, 20])])
        self.assertEqual(response["detection_count"], 1)
        detection = response["detections"][0]
        self.assertEqual(detection["bbox"], dict(x1=0, y1=20, x2=120, y2=80))
        np.testing.assert_array_equal(decode(detection["cropped_image"]), self.image[20:80])

    def test_megapixel_limit_before_inference(self):
        # A broadcast view tests the dimensions without allocating 60 MB.
        oversized = np.broadcast_to(np.zeros((1, 1, 3), np.uint8), (4001, 5000, 3))
        upload = self.upload()
        with patch.object(main.cv2, "imdecode", return_value=oversized), \
                patch.object(main.model, "predict") as predict:
            with self.assertRaises(HTTPException) as error:
                main.process_image(upload)
        self.assertEqual(error.exception.status_code, 413)
        predict.assert_not_called()
        self.assertTrue(upload.file.closed)

    def test_opencv_decode_exception(self):
        upload = self.upload()
        with patch.object(main.cv2, "imdecode", side_effect=cv2.error("bad image")), \
                patch.object(main.model, "predict") as predict:
            with self.assertRaises(HTTPException) as error:
                main.process_image(upload)
        self.assertEqual(error.exception.status_code, 400)
        predict.assert_not_called()
        self.assertTrue(upload.file.closed)


if __name__ == "__main__":
    unittest.main()
