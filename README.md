# AI-Based Nepali Vehicle Number Plate Detection and Recognition System

## Mid-defense prototype

This prototype demonstrates a React image-upload interface connected to FastAPI.
It accepts JPG/JPEG and PNG images, validates and decodes them using OpenCV,
returns the original width and height, and displays a genuine grayscale preview.
The preview's longest side is limited to 1,200 pixels for display; the reported
dimensions belong to the original decoded image.

The interface explicitly shows:

- **YOLO detection: Pending model training**
- **OCR recognition: Pending integration**

No detection, automatic plate cropping, OCR, database, or authentication is
implemented. An image may contain one or multiple plates, but this version only
preprocesses the whole image. It does not return boxes, plate text, or confidence
scores. Uploaded images and results are not persistently saved. FastAPI may
temporarily spool large multipart uploads to the system temporary directory;
the upload is closed after each request. The dataset is never modified.

## Required software and dependencies

- Use the existing Python virtual environment. Its Python version is 3.14.5.
- Python packages: FastAPI (API), Uvicorn (server), python-multipart (uploads),
  NumPy (image byte array), and opencv-python (decode and grayscale conversion).
  OpenCV and NumPy were already present. The other three packages have been
  installed into `.venv`. Package managers also install their required dependencies.
- Install **Node.js 24 LTS for Windows**, including npm, from
  <https://nodejs.org/en/download> if Node.js is not installed. Close and reopen
  your terminal after installing it. You do not need to recreate `.venv`.
- Frontend packages: React and React DOM; Vite is the development/build tool.
  No UI library, router, or additional React build plugin is used.

The local setup was verified with the normally installed Windows Node.js
24.21.0 and npm 11.19.0. No portable Node.js runtime is used.

## Run locally on Windows (PowerShell)

Keep two terminals open. Start the backend first.

### Terminal 1: backend

```powershell
cd C:\FYP\ai-traffic-monitoring-system
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

The explicit Python path uses your existing environment even if the terminal is
not activated. The install command is only needed for initial setup or dependency
changes. If your environment is activated, `python` can replace that path.

- Health check: <http://127.0.0.1:8000/api/health>
- Interactive API documentation: <http://127.0.0.1:8000/docs>

### Terminal 2: frontend

After installing Node.js, open a **new** PowerShell terminal:

```powershell
cd C:\FYP\ai-traffic-monitoring-system\frontend
node --version
npm.cmd --version
npm.cmd install
npm.cmd run dev
```

Open <http://127.0.0.1:5173>. Use `npm.cmd` to avoid PowerShell execution-policy
errors involving `npm.ps1`. `npm.cmd install` is needed only for initial setup or
dependency changes. `frontend/package-lock.json` records the resolved versions.

Vite forwards `/api` requests to FastAPI on port 8000. Both servers must be running.
The frontend uses port 5173 and reports an error if it is occupied. Press Ctrl+C
in each terminal to stop the servers.

## Short demo sequence

1. Open the frontend and point out the two pending AI stages.
2. Select a real JPG or PNG vehicle image and show the original preview.
3. Click **Upload / Process Image**.
4. Show the width, height, format, and OpenCV grayscale result.
5. Explain that the next stage is training YOLO, followed by automatic plate
   cropping and OCR integration.

Files must be at most 10 MB and decoded images at most 20 megapixels. The backend
checks the extension, JPEG/PNG signature, and whether OpenCV can actually decode
the file. Image validation does not verify that an image contains a vehicle.

## Simple code walkthrough for the viva

- `frontend/src/App.jsx`: handles file selection, local preview, upload using
  `FormData`, loading/errors, and results.
- `frontend/vite.config.js`: connects the frontend development server to FastAPI.
- `backend/main.py`: implements `GET /api/health` and `POST /api/process`.
  The upload field is named `file`. OpenCV decodes the bytes, reads `image.shape`,
  optionally resizes the preview, and converts BGR color to grayscale.
- The grayscale image is encoded as PNG and returned as a base64 data URL so
  React can display it without a saved image file or another download endpoint.

## Verification

Verified on this machine: the frontend production build passes, the development
server serves the page, and all five upload tests pass through Vite's API proxy
to FastAPI. Automated visual browser verification was unavailable; manually
follow the short demo sequence above to check the rendered interface.

With the backend running on port 8000, run from the repository root:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The tests use Python's standard library, NumPy, and OpenCV; no separate testing
package is needed. They check the health endpoint, real PNG/JPEG uploads,
dimensions, grayscale pixel values, preview resizing, missing uploads, invalid
formats, corrupted files, empty files, and the 10 MB limit. Test images are made
in memory, without reading or changing the dataset.

To check the frontend build:

```powershell
cd C:\FYP\ai-traffic-monitoring-system\frontend
npm.cmd run build
```

The build writes ignored output into `frontend/dist/`. The documented demo uses
the Vite development server and its API proxy; production hosting is not configured.
