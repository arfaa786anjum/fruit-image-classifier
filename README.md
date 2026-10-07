# Fruit Image Classifier

A full-stack machine learning application to classify images of fruits (Apple, Banana, Orange). This project includes a Convolutional Neural Network (CNN) trained with TensorFlow/Keras, a FastAPI backend for model inference, and a highly polished React UI for end users.

## Features
- **Machine Learning**: Custom CNN trained to recognize apples, bananas, and oranges.
- **Backend API**: FastAPI service providing `/health` and `/predict` endpoints, robust file validation, and optimized model loading.
- **Frontend UI**: A modern, interactive React interface built with Tailwind CSS v4 and Framer Motion, featuring drag-and-drop uploads, sleek animations, and dynamic probability visualization.

## Technology Stack
- **ML Framework**: TensorFlow 2.20.0, Keras, Pillow, NumPy
- **Backend**: FastAPI 0.117.1, Uvicorn, Python 3.12
- **Frontend**: React 18, Vite, Tailwind CSS v4, Framer Motion, Lucide React

## Project Structure
```
.
├── backend/            # FastAPI application and backend tests
├── frontend/           # React + Vite frontend application
├── ml/                 # Model training, dataset prep, and prediction logic
│   ├── models/         # Saved .keras model and metadata
│   ├── reports/        # Training evaluation reports
│   └── tests/          # ML unit tests
├── PROJECT_WORKFLOW.md # Project execution history and requirements
└── README.md           # This file
```

## Prerequisites
- Node.js v24.17.0+
- Python 3.12.0+

## Installation & Setup

1. **Clone the repository**
   (Assuming you are in the project root directory)

2. **Backend Setup**
   ```bash
   pip install -r backend/requirements.txt
   pip install -r ml/requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

## Running the Application

1. **Start the Backend API** (Run in a separate terminal)
   ```bash
   uvicorn backend.main:app --reload --port 8000
   ```
   *The API will be available at `http://localhost:8000`*

2. **Start the Frontend UI** (Run in a separate terminal)
   ```bash
   cd frontend
   npm run dev
   ```
   *The application will open at `http://localhost:5173`*

## Dataset & Training
This project currently uses a generated synthetic mock dataset (solid RGB blocks) for the purpose of rapid prototyping and pipeline validation, bypassing external download constraints.
- **Classes**: `apple` (red), `banana` (yellow), `orange` (orange).
- **Training command**: `python ml/train.py`
- **Evaluation command**: `python ml/evaluate.py`
- **Actual test accuracy**: 100% (Note: This is strictly on the synthetic dataset).

## Testing
- **ML Pipeline tests**: `python -m unittest discover -s ml/tests`
- **Backend API tests**: `python -m unittest discover -s backend/tests`
- **Frontend Build test**: `cd frontend && npm run build`

## Known Limitations & Troubleshooting
- **Real-World Generalization**: Because the model was trained on synthetic distinct color blocks (mock data), it will incorrectly classify actual photographs of fruit. To fix this, replace the images in `ml/dataset/train` with real fruit images and re-run `python ml/train.py`.
- **CORS Configuration**: The backend currently only allows requests from `http://localhost:5173` (and `127.0.0.1:5173`). If your Vite dev server uses a different port, update the `origins` list in `backend/main.py`.
