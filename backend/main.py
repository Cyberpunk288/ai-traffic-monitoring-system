"""Image upload, preprocessing, and trained YOLO license plate detection."""

import base64
from pathlib import Path
from threading import Lock

import cv2
import numpy as np

# Compatibility for the pure-Python python-bidi 0.4.2 package.
# EasyOCR expects get_display to be available directly from bidi.
import bidi
from bidi.algorithm import get_display

if not hasattr(bidi, "get_display"):
    bidi.get_display = get_display

import easyocr
from fastapi import FastAPI, HTTPException, UploadFile
from ultralytics import YOLO

from backend.database import (
    get_detection_history,
    initialize_database,
    save_detection,
)

app = FastAPI(title="Nepali Vehicle Number Plate - Upload Prototype")

initialize_database()

# Load once per backend process, independently of the working directory.
MODEL_PATH = Path(__file__).resolve().parents[1] / "ai" / "models" / "best.pt"

model = YOLO(str(MODEL_PATH))

# Load EasyOCR once when the backend starts.
ocr_reader = easyocr.Reader(["ne"], gpu=False)

inference_lock = Lock()
ocr_lock = Lock()

MAX_FILE_BYTES = 10 * 1024 * 1024
MAX_IMAGE_PIXELS = 20_000_000
PREVIEW_MAX_SIDE = 1200

def recognize_plate_text(plate_image):
    """Run EasyOCR on a detected plate crop and return text with confidence."""

    if plate_image is None or plate_image.size == 0:
        return {
            "text": None,
            "confidence": 0.0,
            "status": "uncertain",
        }

    # Enlarge small plate crops before OCR.
    enlarged = cv2.resize(
        plate_image,
        None,
        fx=4,
        fy=4,
        interpolation=cv2.INTER_CUBIC,
    )

    # Grayscale gives OCR a simpler input.
    grayscale = cv2.cvtColor(enlarged, cv2.COLOR_BGR2GRAY)

    with ocr_lock:
        results = ocr_reader.readtext(
            grayscale,
            detail=1,
            paragraph=False,
        )

    if not results:
        return {
            "text": None,
            "confidence": 0.0,
            "status": "uncertain",
        }

    # Keep the detected pieces in EasyOCR's returned order.
    text_parts = []
    confidences = []

    for result in results:
        text = result[1].strip()
        confidence = float(result[2])

        if text:
            text_parts.append(text)
            confidences.append(confidence)

    if not text_parts:
        return {
            "text": None,
            "confidence": 0.0,
            "status": "uncertain",
        }

    combined_text = " ".join(text_parts)
    average_confidence = sum(confidences) / len(confidences)

    # Do not present weak OCR as a trustworthy plate number.
    status = "recognized" if average_confidence >= 0.50 else "uncertain"

    return {
        "text": combined_text,
        "confidence": average_confidence,
        "status": status,
    }


def png_data_url(image):
    success, encoded = cv2.imencode(".png", image)
    if not success:
        raise HTTPException(500, "Could not encode a detection image.")
    return "data:image/png;base64," + base64.b64encode(encoded).decode("ascii")


@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/history")
def history():
    """Return the most recent saved plate detection records."""
    return {
        "records": get_detection_history(limit=50)
    }


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

        # FastAPI can run uploads concurrently; protect the shared predictor.
        with inference_lock:
            result = model.predict(source=image, conf=0.25, save=False, verbose=False)[0]

        detections = []
        annotated = image.copy()
        for box in result.boxes:
            coordinates = box.xyxy[0].tolist()
            # Round outward and clip to the image for safe, nonempty crops.
            x1 = max(0, min(width, int(np.floor(coordinates[0]))))
            y1 = max(0, min(height, int(np.floor(coordinates[1]))))
            x2 = max(0, min(width, int(np.ceil(coordinates[2]))))
            y2 = max(0, min(height, int(np.ceil(coordinates[3]))))
            if x2 <= x1 or y2 <= y1:
                continue
            confidence = float(box.conf[0])
            class_name = result.names[int(box.cls[0])]

            plate_crop = image[y1:y2, x1:x2]
            ocr_result = recognize_plate_text(plate_crop)

            save_detection(
                filename=file.filename or "unknown",
                plate_text=ocr_result["text"],
                detection_confidence=confidence,
                ocr_confidence=ocr_result["confidence"],
                ocr_status=ocr_result["status"],
            )


            detections.append({
                "class_name": class_name,
                "confidence": confidence,
                "bbox": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
                "cropped_image": png_data_url(plate_crop),
                 "ocr": ocr_result,
            })
            cv2.rectangle(annotated, (x1, y1), (x2 - 1, y2 - 1), (0, 255, 0), 2)
            cv2.putText(annotated, f"{class_name} {confidence:.2f}",
                        (x1, max(15, y1 - 6)), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 1, cv2.LINE_AA)

        return {
            "width": width,
            "height": height,
            "format": "PNG" if is_png else "JPEG",
            "size_bytes": len(contents),
            "grayscale_image": "data:image/png;base64," + base64.b64encode(encoded).decode("ascii"),
            "detection_count": len(detections),
            "detections": detections,
            "annotated_image": png_data_url(annotated),
        }
    finally:
        file.file.close()
