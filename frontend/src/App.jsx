import React, { useEffect, useState } from 'react';

export default function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [processing, setProcessing] = useState(false);

  useEffect(() => {
    if (!file) {
      setPreview('');
      return;
    }
    const url = URL.createObjectURL(file);
    setPreview(url);
    return () => URL.revokeObjectURL(url);
  }, [file]);

  function selectImage(event) {
    const selected = event.target.files[0];
    setResult(null);
    setError('');
    setFile(null);
    if (!selected) return;
    if (!/\.(jpe?g|png)$/i.test(selected.name)) {
      setError('Please select a JPG or PNG image.');
      event.target.value = '';
      return;
    }
    if (selected.size > 10 * 1024 * 1024) {
      setError('The image must be 10 MB or smaller.');
      event.target.value = '';
      return;
    }
    setFile(selected);
  }

  async function processImage(event) {
    event.preventDefault();
    if (!file || processing) return;
    setProcessing(true);
    setResult(null);
    setError('');
    const form = new FormData();
    form.append('file', file);
    try {
      const response = await fetch('/api/process', {
        method: 'POST',
        body: form,
        signal: AbortSignal.timeout(30000),
      });
      const data = await response.json().catch(() => null);
      if (!response.ok) {
        throw new Error(typeof data?.detail === 'string'
          ? data.detail : 'Processing failed. Check that the FastAPI backend is running.');
      }
      if (!data) throw new Error('The backend returned an invalid response.');
      setResult(data);
    } catch (err) {
      setError(err.name === 'TimeoutError'
        ? 'The request timed out. Please check the backend and try again.'
        : err instanceof TypeError
          ? 'Cannot reach the backend. Start FastAPI and try again.'
          : err.message);
    } finally {
      setProcessing(false);
    }
  }

  return (
    <main>
      <header>
        <p className="eyebrow">FINAL YEAR PROJECT · MID-DEFENSE PROTOTYPE</p>
        <h1>AI-Based Nepali Vehicle Number Plate Detection and Recognition System</h1>
        <p className="intro">Upload a vehicle image to detect and crop license plates with YOLO and explore OpenCV grayscale preprocessing. OCR recognition is pending integration.</p>
      </header>

      <section className="pipeline" aria-label="Development status">
        <span className="ready">Image upload &amp; preprocessing: Available</span>
        <span className="ready">YOLO plate detection: Available</span>
        <span>OCR recognition: Pending integration</span>
      </section>

      <section className="card">
        <h2>Upload a vehicle image</h2>
        <form onSubmit={processImage}>
          <label htmlFor="vehicle-image">Choose image</label>
          <input id="vehicle-image" type="file" accept=".jpg,.jpeg,.png,image/jpeg,image/png"
            onChange={selectImage} disabled={processing} aria-describedby="file-help" />
          <p id="file-help" className="muted">JPG or PNG · Up to 10 MB and 20 megapixels</p>
          <button type="submit" disabled={!file || processing}>
            {processing ? 'Processing image…' : 'Upload / Process Image'}
          </button>
        </form>
        {error && <p className="error" role="alert">{error}</p>}
        <p className="status" role="status">
          {processing ? 'Uploading, detecting license plates, and preparing previews…'
            : result ? 'Image validated and processed successfully.' : ''}
        </p>
        {result && (
          <dl className="metadata">
            <div><dt>Original width</dt><dd>{result.width.toLocaleString()} px</dd></div>
            <div><dt>Original height</dt><dd>{result.height.toLocaleString()} px</dd></div>
            <div><dt>Format</dt><dd>{result.format}</dd></div>
          </dl>
        )}
      </section>

      <section className="previews" aria-label="Image previews">
        <article className="card">
          <h2>Selected image</h2>
          {preview ? <img src={preview} alt="Selected vehicle" onError={() => {
            setPreview('');
            setError('This file cannot be previewed. Select a valid JPG or PNG image.');
            setFile(null);
          }} /> : <div className="placeholder">Your selected image will appear here.</div>}
        </article>
        <article className="card">
          <h2>YOLO Detection Result</h2>
          {result ? (
            <>
              <img src={result.annotated_image} alt="YOLO detection result with bounding boxes and confidence values for detected plates" />
              <p className="detection-count">Detected plates: <strong>{result.detection_count}</strong></p>
              {result.detection_count === 0 && <p className="muted">No license plate detected.</p>}
            </>
          ) : <div className="placeholder">Process an image to see the YOLO detection result.</div>}
        </article>
      </section>

      {result && result.detections.length > 0 && (
        <section className="plate-results" aria-labelledby="detected-plates-title">
          <h2 id="detected-plates-title">Detected plates</h2>
          <div className="plate-grid">
            {result.detections.map((detection, index) => (
              <article className="card plate-card" key={index}>
                <h3>Plate {index + 1}</h3>
                <img src={detection.cropped_image} alt={`Cropped license plate ${index + 1}`} />
                <dl className="plate-details">
                  <div><dt>Class</dt><dd>{detection.class_name}</dd></div>
                  <div><dt>Confidence</dt><dd>{(detection.confidence * 100).toFixed(1)}%</dd></div>
                  <div className="plate-bbox">
                    <dt>Bounding box (original image pixels)</dt>
                    <dd>x1: {detection.bbox.x1}, y1: {detection.bbox.y1}, x2: {detection.bbox.x2}, y2: {detection.bbox.y2}</dd>
                  </div>
                </dl>
              </article>
            ))}
          </div>
        </section>
      )}

      <section className="previews preprocessing" aria-label="Full-image preprocessing preview">
        <article className="card">
          <h2>OpenCV grayscale — full-image preview</h2>
          {result ? <img src={result.grayscale_image} alt="Grayscale version generated by OpenCV" />
            : <div className="placeholder">Process an image to see the grayscale output.</div>}
          <p className="muted">This preprocessing preview shows the full image in grayscale. It is resized to at most 1,200 pixels on its longest side. OCR recognition is pending integration.</p>
        </article>
      </section>
      <footer>This prototype demonstrates YOLO plate detection, automatic plate cropping, and OpenCV preprocessing. OCR character recognition is pending integration. Uploaded images are not saved by this application.</footer>
    </main>
  );
}
