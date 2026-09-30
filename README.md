# AI-Based Nepali Vehicle Number Plate Detection and Recognition System

A Final Year Project that detects Nepali vehicle number plates from uploaded images using YOLOv8n, performs OCR using EasyOCR with OpenCV preprocessing, and stores detection history in SQLite.

## Features

- Upload JPG/PNG vehicle images
- Detect one or multiple number plates
- Automatic plate cropping
- YOLOv8n plate detection
- OpenCV skew-aware preprocessing
- EasyOCR with Devanagari support
- OCR confidence and uncertainty status
- Annotated detection output
- Detection history stored in SQLite
- React frontend with FastAPI backend

## System Pipeline

React Frontend
→ FastAPI Backend
→ YOLOv8n Detection
→ Plate Cropping
→ OpenCV Preprocessing
→ EasyOCR
→ SQLite History
→ Results Display

## Technology Stack

### Frontend
- React.js
- Vite
- JavaScript
- CSS

### Backend
- Python
- FastAPI
- Uvicorn

### AI / Computer Vision
- YOLOv8n
- Ultralytics
- OpenCV
- EasyOCR
- NumPy
- PyTorch

### Database
- SQLite

SQLite is currently used as local prototype persistence. PostgreSQL was originally intended, but local PostgreSQL initialization was blocked by Windows Application Control.

## Dataset

Total dataset:
- Images: 8,078
- YOLO label files: 8,078

Dataset split:
- Training: 5,654
- Validation: 1,615
- Test: 809

Dataset validation:
- Missing labels: 0
- Labels without images: 0
- Invalid annotations: 0
- Invalid class IDs: 0
- Invalid coordinates: 0
- Corrupted images: 0

## YOLO Training

Model:
- YOLOv8n
- Pretrained model fine-tuned using transfer learning
- 100 epochs
- Training environment: Google Colab T4 GPU

### Detection Results

Held-out test set:
- 809 images
- 879 number plate instances

Metrics:
- Precision: 97.1%
- Recall: 95.7%
- mAP@0.5: 98.9%
- mAP@0.5:0.95: 92.8%
- Inference: 2.9 ms/image on Google Colab T4

These metrics evaluate number plate detection only and are not OCR accuracy.

## OCR

OCR pipeline:
1. YOLO detects the plate
2. Plate is automatically cropped
3. Skew is estimated using OpenCV
4. Reliable skew is corrected
5. Crop is enlarged
6. Converted to grayscale
7. EasyOCR performs recognition

OCR confidence is displayed separately from recognition correctness.

### OCR Evaluation

A manually verified eight-image evaluation set was used.

Baseline mean Character Error Rate:
- 90.66%

Selected skew-aware preprocessing:
- Mean CER: 73.88%

Improvement:
- 16.78 percentage-point CER reduction
- Improved: 7/8 images
- Tied: 1/8
- Worsened: 0/8

Exact full-plate matches:
- 0/8

OCR therefore remains a limitation of the current system.

## Database

Table:

`detection_history`

Fields:
- `id`
- `filename`
- `plate_text`
- `detection_confidence`
- `ocr_confidence`
- `ocr_status`
- `created_at`

Uploaded original image files are not permanently stored.

## API Endpoints

### Health Check

```text
GET /api/health