"""Image upload and real OpenCV preprocessing for the mid-defense demo."""

import base64
from pathlib import Path

import cv2
import numpy as np
from fastapi import FastAPI, HTTPException, UploadFile

app = FastAPI(title="Nepali Vehicle Number Plate — Upload Prototype")

MAX_FILE_BYTES = 10 * 1024 * 1024
MAX_IMAGE_PIXELS = 20_000_000
PREVIEW_MAX_SIDE = 1200


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/process")
def process_image(file: UploadFile):
    # The original file is never saved to the project or dataset.
    try:
        extension = Path(file.filename or "").suffix.lower()
        if extension not in {".jpg", ".jpeg", ".png"}:
            raise HTTPException(400, "Please upload a JPG or PNG image.")

        contents = file.file.read(MAX_FILE_BYTES + 1)
        if not contents:
            raise HTTPException(400, "The uploaded file is empty.")
        if len(contents) > MAX_FILE_BYTES:
            raise HTTPException(413, "The image must be 10 MB or smaller.")

        # Check the actual format as well as the extension. A renamed text
        # file, GIF, etc. must not be accepted as a JPG or PNG.
        is_jpeg = contents.startswith(b"\xff\xd8\xff")
        is_png = contents.startswith(b"\x89PNG\r\n\x1a\n")
        if not ((extension in {".jpg", ".jpeg"} and is_jpeg)
                or (extension == ".png" and is_png)):
            raise HTTPException(400, "The file contents must match its JPG or PNG extension.")

        try:
            image = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)
        except cv2.error:
            image = None
        if image is None:
            raise HTTPException(400, "OpenCV could not read this image. It may be damaged.")

        height, width = image.shape[:2]
        if width * height > MAX_IMAGE_PIXELS:
            raise HTTPException(413, "Please choose an image with 20 megapixels or fewer.")

        # Resize only the preview; the reported dimensions are the original's.
        scale = min(1.0, PREVIEW_MAX_SIDE / max(width, height))
        preview = image
        if scale < 1:
            preview = cv2.resize(image, (max(1, round(width * scale)),
                                         max(1, round(height * scale))),
                                 interpolation=cv2.INTER_AREA)
        grayscale = cv2.cvtColor(preview, cv2.COLOR_BGR2GRAY)
        success, encoded = cv2.imencode(".png", grayscale)
        if not success:
            raise HTTPException(500, "Could not generate the grayscale preview.")

        return {
            "width": width,
            "height": height,
            "format": "PNG" if is_png else "JPEG",
            "size_bytes": len(contents),
            "grayscale_image": "data:image/png;base64," + base64.b64encode(encoded).decode("ascii"),
        }
    finally:
        file.file.close()
