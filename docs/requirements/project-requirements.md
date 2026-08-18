# 3.2 System Requirement Specification (SRS)

## 3.2.1 System Overview

The AI-Based Nepali Vehicle Number Plate Detection and Recognition System is a web-based application designed to detect and recognize Nepali vehicle number plates from uploaded images.

The system allows a user to upload an image containing a vehicle through a React.js web interface. The uploaded image is processed by a FastAPI backend, where computer vision and an AI-based number plate detection model are used to identify the number plate region. The detected plate is then processed and passed to an Optical Character Recognition (OCR) component to extract the characters present on the plate.

The recognized plate information, confidence score, image reference, and processing timestamp are stored in a PostgreSQL database. Users can view the recognition result immediately and access previously processed records through a history interface.

The system is designed as an image-upload-based prototype. Real-time video processing, vehicle tracking, and traffic violation detection are outside the current scope and are considered future enhancements.

## 3.2.2 User Requirements

The system shall provide a simple web interface that allows users to:

1. Upload an image containing a Nepali vehicle.
2. Submit the image for number plate processing.
3. View the detected number plate region.
4. View the recognized number plate text.
5. View the confidence score of the recognition result.
6. View previously processed recognition records.
7. Identify errors when an image is invalid or no number plate is detected.

The system should not require the user to have technical knowledge about image processing, artificial intelligence, or OCR.

## 3.2.3 Functional Requirements

The functional requirements define the operations and services that the system shall provide.

### FR-01: Image Upload

The system shall allow the user to upload an image containing a vehicle through the web interface.

Supported image formats shall include:

- JPEG
- JPG
- PNG

### FR-02: Image Validation

The system shall validate the uploaded image before processing.

The system shall reject unsupported file formats or invalid image files and display an appropriate error message to the user.

### FR-03: Image Pre-processing

The system shall perform image pre-processing using computer vision techniques before number plate detection.

The pre-processing may include:

- Image resizing
- Grayscale conversion
- Noise reduction
- Contrast enhancement
- Image normalization

### FR-04: Number Plate Detection

The system shall use an AI-based number plate detection model to identify and localize the Nepali vehicle number plate within the uploaded image.

The detection model shall be trained or fine-tuned using an appropriate dataset and evaluated using suitable object-detection metrics.

### FR-05: Plate Region Extraction

The system shall crop or extract the detected number plate region from the original image for further processing.

### FR-06: OCR Processing

The system shall process the detected plate region using an Optical Character Recognition (OCR) technique to extract the characters present on the number plate.

The OCR component shall support the relevant Devanagari and Arabic/numeric characters used in Nepali vehicle number plates.

### FR-07: Recognition Post-processing

The system shall clean and validate the OCR output to reduce incorrect or malformed recognition results.

The system shall apply appropriate rules based on the expected structure of Nepali vehicle number plates.

### FR-08: Recognition Result

The system shall display the following information to the user after successful processing:

- Original uploaded image
- Detected/cropped number plate image
- Recognized plate number
- Recognition confidence score
- Processing timestamp

### FR-09: Database Storage

The system shall store successful recognition records in the PostgreSQL database.

Each record shall contain, where applicable:

- Unique record ID
- Image reference
- Detected plate text
- Confidence score
- Processing timestamp

### FR-10: Recognition History

The system shall allow the user to view previously processed recognition records.

The history shall display relevant information such as the recognized plate number, confidence score, and processing date.

### FR-11: Error Handling

The system shall provide appropriate error messages when:

- An unsupported file is uploaded.
- An invalid image is uploaded.
- No number plate is detected.
- OCR fails to produce a usable result.
- A database or server error occurs.

### FR-12: REST API

The FastAPI backend shall provide RESTful API endpoints for:

- Image upload and processing
- Recognition result retrieval
- Recognition history retrieval
- Error response handling

### FR-13: AI Model Evaluation

The system development process shall include evaluation of the trained or fine-tuned AI model using appropriate evaluation metrics.

The evaluation results shall be documented as part of the AI model training and evaluation documentation.

### FR-14: User Interface

The React.js frontend shall provide interfaces for:

- Image upload
- Processing status
- Recognition result display
- Recognition history
- Error messages

### FR-15: Deployment

The completed application shall be deployable on a suitable local server or cloud environment.

## 3.2.4 Non-Functional Requirements

The non-functional requirements define the quality attributes and operational constraints of the system.

### NFR-01: Performance

The system should process a typical uploaded image and return a recognition result within a few seconds under normal operating conditions.

The system should avoid unnecessary processing and use efficient image-processing and AI inference techniques.

### NFR-02: Accuracy

The AI-based number plate detection and OCR components should achieve measurable and acceptable performance on the selected Nepali vehicle number plate dataset.

The performance of the AI model shall be evaluated using appropriate metrics and documented in the AI Model Training and Evaluation Report.

### NFR-03: Usability

The system shall provide a simple and intuitive web interface.

A user should be able to upload an image and understand the recognition result without requiring technical knowledge of artificial intelligence or computer vision.

### NFR-04: Reliability

The system should process valid image files consistently without unexpected crashes.

When an error occurs, the system should provide an appropriate error message instead of terminating unexpectedly.

### NFR-05: Maintainability

The application shall use a modular architecture that separates:

- Frontend
- Backend API
- AI model and inference
- Image processing
- OCR
- Database operations

This structure should allow individual components to be modified or replaced without requiring major changes to the entire system.

### NFR-06: Security

The system shall implement basic security measures for uploaded files and API requests.

These measures shall include:

- File type validation
- File size validation
- Safe file handling
- Input validation
- Protection against invalid or malicious requests

Sensitive configuration information such as database credentials shall not be stored directly in the source code.

### NFR-07: Portability

The system should be capable of running on common development environments such as Windows and Linux.

The application should also be suitable for deployment to a cloud or local server environment.

### NFR-08: Scalability

The system architecture should allow future expansion to support additional features such as:

- Multiple vehicles per image
- Real-time webcam processing
- Video processing
- Vehicle tracking
- Traffic violation detection

These features are outside the current implementation scope but should be considered when designing the system.

### NFR-09: Availability

The deployed application should be available to authorized users whenever the hosting environment is operational.

For local deployment, availability will depend on the availability of the host machine and network.

### NFR-10: Compatibility

The web application should operate correctly on modern web browsers such as:

- Google Chrome
- Microsoft Edge
- Mozilla Firefox

### NFR-11: Documentation

The project shall maintain complete technical and academic documentation, including:

- System requirements
- System architecture
- Database design
- AI model training process
- AI model evaluation
- Testing results
- Deployment procedure
- User instructions

### NFR-12: Version Control

All source code and major development changes shall be maintained using Git and GitHub.

The repository shall follow the college requirements for meaningful commits and branch-based development.

The project shall maintain regular development history rather than uploading the complete project only at the end of development.

## 3.2.5 Hardware Requirements

The following hardware is recommended for development, testing, and local deployment of the system.

| Component | Minimum Requirement | Recommended |
|---|---|---|
| Processor | Intel Core i5 / AMD Ryzen 5 or equivalent | Intel Core i5/i7 or AMD Ryzen 5/7 |
| RAM | 8 GB | 16 GB |
| Storage | 5 GB free space | 20 GB or more |
| GPU | Not mandatory | NVIDIA GPU with CUDA support |
| Display | 1366 × 768 resolution | Full HD (1920 × 1080) |
| Internet | Required for development and dependency installation | Stable broadband connection |

### Hardware Notes

The system can be developed and tested without a dedicated GPU. CPU-based processing is sufficient for initial development and testing.

A compatible GPU may be used to accelerate AI model training and inference if required.

Additional storage may be required depending on the size of the training dataset, trained model files, uploaded images, and project artifacts.

## 3.2.6 Software Requirements

The following software technologies and development tools will be used in the project.

| Category | Technology |
|---|---|
| Operating System | Windows 10/11 or Ubuntu 20.04+ |
| Programming Language | Python 3.10+ |
| Frontend | React.js |
| Backend | FastAPI |
| Database | PostgreSQL 14+ |
| Computer Vision | OpenCV |
| AI/ML | Python-based deep learning/object detection framework |
| OCR | EasyOCR / Tesseract OCR, subject to evaluation |
| API Testing | Postman |
| IDE | Visual Studio Code |
| Version Control | Git |
| Repository | GitHub |
| Deployment | Docker and/or suitable cloud/local server |
| Database ORM | SQLAlchemy |
| API Server | Uvicorn |

### Development Environment

The project will be developed using Visual Studio Code. Python virtual environments will be used to isolate project dependencies.

The backend will be developed using FastAPI and served during development using Uvicorn.

PostgreSQL will be used as the primary relational database.

The React.js application will provide the user-facing web interface and communicate with the FastAPI backend through RESTful APIs.

Git and GitHub will be used for source-code management, branch-based development, documentation, and tracking of project progress.

## 3.2.7 AI/ML Requirements

The AI/ML component is a mandatory part of the system and shall be responsible for detecting Nepali vehicle number plates from uploaded images.

### AI-01: AI-Based Number Plate Detection

The system shall use a trained or fine-tuned object-detection model to identify and localize Nepali vehicle number plates within uploaded images.

The model shall produce a bounding box indicating the detected plate region and a confidence score for the detection.

### AI-02: Dataset Requirement

A suitable dataset containing images of Nepali vehicles and number plates shall be collected or obtained from legally usable sources.

The dataset shall represent different realistic conditions, including variations in:

- Vehicle types
- Plate sizes
- Viewing angles
- Image resolutions
- Lighting conditions
- Background environments
- Plate appearance

The dataset shall be documented, organized, and separated into training, validation, and testing subsets.

### AI-03: Dataset Annotation

Images used for supervised number plate detection training shall be annotated with bounding boxes around the number plate regions.

The annotation format shall be compatible with the selected object-detection framework.

The dataset preparation and annotation process shall be documented.

### AI-04: Model Training

The selected AI model shall be trained or fine-tuned using the prepared dataset.

The training process shall include appropriate configuration of:

- Training dataset
- Validation dataset
- Number of training epochs
- Batch size
- Learning rate or other relevant hyperparameters
- Model architecture
- Evaluation criteria

The final training configuration shall be documented.

### AI-05: Training from Scratch or Fine-Tuning

The final training strategy shall be selected according to the project requirements and institutional guidelines.

If pretrained weights are permitted, an appropriate pretrained model may be fine-tuned using the Nepali number plate dataset.

If pretrained weights are not permitted, the selected model shall be trained from randomly initialized weights using the prepared dataset.

The selected approach and its justification shall be documented.

### AI-06: Model Evaluation

The trained model shall be evaluated using an independent test dataset that is not used during model training.

Appropriate object-detection evaluation metrics may include:

- Precision
- Recall
- F1-score
- Intersection over Union (IoU)
- Mean Average Precision (mAP)

The final evaluation results shall be documented and analyzed.

### AI-07: OCR Recognition

The detected number plate region shall be processed using an OCR technique to recognize the characters present on the plate.

The OCR component shall be evaluated using representative Nepali number plate images.

The project shall investigate the ability of the selected OCR approach to recognize the Devanagari and numeric characters used on Nepali vehicle number plates.

### AI-08: Image Pre-processing

The system may apply image-processing techniques before detection and OCR to improve recognition performance.

Possible techniques include:

- Resizing
- Grayscale conversion
- Noise reduction
- Contrast enhancement
- Thresholding
- Sharpening
- Perspective correction

The effectiveness of relevant pre-processing techniques shall be evaluated where appropriate.

### AI-09: Post-processing

The OCR output shall undergo post-processing to remove unnecessary characters, correct formatting issues, and validate the recognized text against the expected structure of Nepali vehicle number plates.

### AI-10: Model Storage

The trained AI model shall be saved as a versioned model artifact and stored separately from the application source code where appropriate.

The model version used by the application shall be documented.

### AI-11: Inference

The backend shall load the trained model during inference and use it to process uploaded images.

The inference pipeline shall return the detected plate region and associated confidence information to the application.

### AI-12: AI Documentation

The project shall maintain documentation covering:

1. Dataset source and characteristics
2. Dataset preparation and annotation
3. Data splitting strategy
4. Model architecture
5. Training configuration
6. Training results
7. Evaluation metrics
8. Model comparison, where applicable
9. Error analysis
10. Final model selection

The AI training and evaluation documentation shall form part of the final project report and supporting project documentation.

## 3.2.8 Database Requirements

PostgreSQL shall be used as the primary relational database management system for storing recognition records and related application data.

### DB-01: Recognition Records

The database shall store information associated with each successfully processed image.

A recognition record shall contain, where applicable:

- Unique record ID
- Image reference/path
- Recognized plate number
- Detection confidence score
- OCR confidence score, where available
- Processing timestamp

### DB-02: Record Retrieval

The system shall allow the backend to retrieve previously stored recognition records.

The retrieved records shall be provided to the frontend through RESTful API endpoints.

### DB-03: Record Listing

The system shall provide functionality to retrieve a list of previously processed recognition records for display in the frontend history interface.

### DB-04: Data Integrity

The database shall enforce appropriate constraints to maintain data integrity.

These may include:

- Primary keys
- Appropriate data types
- NOT NULL constraints where required
- Foreign keys where relationships exist
- Appropriate indexes

### DB-05: Database Access

The FastAPI backend shall communicate with PostgreSQL through an appropriate database access layer or ORM.

SQLAlchemy shall be used to manage database models and database interactions.

### DB-06: Database Configuration

Database connection information shall be stored securely using environment variables rather than being hard-coded in the application source code.

### DB-07: Database Documentation

The project shall document the database structure using an Entity Relationship Diagram (ERD) and database schema.

The final database design shall be included in the System Design chapter of the project report.

## 3.2.8 Database Requirements

PostgreSQL shall be used as the primary relational database management system for storing recognition records and related application data.

### DB-01: Recognition Records

The database shall store information associated with each successfully processed image.

A recognition record shall contain, where applicable:

- Unique record ID
- Image reference/path
- Recognized plate number
- Detection confidence score
- OCR confidence score, where available
- Processing timestamp

### DB-02: Record Retrieval

The system shall allow the backend to retrieve previously stored recognition records.

The retrieved records shall be provided to the frontend through RESTful API endpoints.

### DB-03: Record Listing

The system shall provide functionality to retrieve a list of previously processed recognition records for display in the frontend history interface.

### DB-04: Data Integrity

The database shall enforce appropriate constraints to maintain data integrity.

These may include:

- Primary keys
- Appropriate data types
- NOT NULL constraints where required
- Foreign keys where relationships exist
- Appropriate indexes

### DB-05: Database Access

The FastAPI backend shall communicate with PostgreSQL through an appropriate database access layer or ORM.

SQLAlchemy shall be used to manage database models and database interactions.

### DB-06: Database Configuration

Database connection information shall be stored securely using environment variables rather than being hard-coded in the application source code.

### DB-07: Database Documentation

The project shall document the database structure using an Entity Relationship Diagram (ERD) and database schema.

The final database design shall be included in the System Design chapter of the project report.

## 3.2.9 Security Requirements

The system shall implement basic security controls to protect the application, uploaded files, API endpoints, and stored data.

### SEC-01: File Validation

The backend shall validate uploaded files before processing.

Validation shall include:

- File extension
- MIME type where appropriate
- File size
- Image readability

### SEC-02: Secure File Handling

Uploaded files shall be handled using controlled storage locations.

The system shall avoid executing uploaded files as code.

### SEC-03: Input Validation

User-provided input received through API requests shall be validated before being processed or stored.

### SEC-04: Database Credentials

Database credentials and other sensitive configuration values shall not be committed to GitHub.

Environment variables or an appropriate configuration mechanism shall be used to store sensitive information.

### SEC-05: Environment Configuration

Development secrets shall be stored in a local `.env` file or equivalent secure configuration mechanism.

The `.env` file shall be excluded from Git version control using `.gitignore`.

### SEC-06: API Security

The backend shall validate API requests and return appropriate HTTP status codes for invalid or unauthorized requests.

### SEC-07: Error Handling

The system shall not expose sensitive implementation details, database credentials, file-system information, or internal stack traces to end users.

### SEC-08: Dependency Management

Project dependencies shall be documented and managed using a requirements file or appropriate package-management mechanism.

Dependencies shall be reviewed and updated when necessary to reduce security risks.

## 3.2.10 Deployment Requirements

The completed system shall be capable of being deployed on a local server or a suitable cloud hosting environment.

### DEP-01: Backend Deployment

The FastAPI backend shall be deployable using an ASGI server such as Uvicorn.

### DEP-02: Frontend Deployment

The React.js frontend shall be buildable into production-ready static assets and deployable to a suitable web hosting environment.

### DEP-03: Database Deployment

The PostgreSQL database shall be deployable either on the same server as the application for local deployment or through a managed/cloud database service.

### DEP-04: AI Model Deployment

The trained AI model and required OCR components shall be included in the deployment environment so that the application can perform inference without requiring model training during normal operation.

### DEP-05: Environment Configuration

Deployment-specific configuration values, including database connection details and other sensitive settings, shall be provided through environment variables.

### DEP-06: Containerization

Docker may be used to package the frontend, backend, AI dependencies, and supporting services into reproducible deployment environments.

### DEP-07: Deployment Documentation

The project shall document the deployment process, including:

- Environment setup
- Dependency installation
- Database configuration
- AI model configuration
- Backend configuration
- Frontend configuration
- Application startup
- Required environment variables

### DEP-08: Deployment Testing

The deployed application shall be tested to verify that:

- The frontend loads correctly.
- The backend API is accessible.
- The database connection works correctly.
- The AI model can perform inference.
- Image upload and recognition work correctly.
- Recognition records can be stored and retrieved.