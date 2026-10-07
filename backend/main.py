import os
import sys
import logging
import tempfile
import pathlib
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Add project root to path to import ml.predict
SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.append(str(PROJECT_ROOT))

from ml.predict import FruitPredictor

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
SUPPORTED_FORMATS = {"image/jpeg", "image/png", "image/jpg"}

# Initialize app and predictor
app = FastAPI(title="Fruit Image Classifier API", description="API to predict fruit classes from images.")
predictor = FruitPredictor()

# CORS configuration
origins = [
    "http://localhost:5173", # Vite dev server
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    try:
        logger.info("Loading ML model...")
        predictor.load_model()
        logger.info("ML model loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load ML model: {e}")

@app.get("/health")
async def health_check():
    """Returns the health status of the API and the underlying model."""
    model_ready = predictor.model is not None
    return {
        "status": "healthy" if model_ready else "degraded",
        "model_loaded": model_ready
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Predicts the fruit class from an uploaded image."""
    # 1. Validate Model State
    if predictor.model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded or unavailable.")
    
    # 2. Validate MIME Type
    if file.content_type not in SUPPORTED_FORMATS:
        raise HTTPException(status_code=415, detail=f"Unsupported file format: {file.content_type}. Please upload a JPEG or PNG.")
        
    # 3. Validate File Size
    try:
        contents = await file.read()
    except Exception:
        raise HTTPException(status_code=400, detail="Error reading file.")
        
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail=f"File too large. Maximum size is {MAX_FILE_SIZE/(1024*1024)}MB.")
        
    # Write to a temporary file for the predictor to open
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(contents)
            tmp_path = tmp.name
            
        # 4. Predict
        try:
            result = predictor.predict_image(tmp_path)
            return result
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise HTTPException(status_code=422, detail="Invalid or corrupt image data. Could not process image.")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Internal error during prediction: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
