import os
import sys
import pathlib
import unittest
from io import BytesIO
from PIL import Image

# Add project root to path
SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
sys.path.append(str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from backend.main import app

class TestPredictionAPI(unittest.TestCase):
    
    def test_health_check(self):
        # Using context manager explicitly triggers startup/shutdown events
        with TestClient(app) as client:
            response = client.get("/health")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("status", data)
            self.assertIn("model_loaded", data)
            self.assertTrue(data["model_loaded"])
            self.assertEqual(data["status"], "healthy")

    def test_predict_valid_image(self):
        img = Image.new("RGB", (100, 100), color=(255, 0, 0))
        img_bytes = BytesIO()
        img.save(img_bytes, format="JPEG")
        img_bytes.seek(0)
        
        with TestClient(app) as client:
            response = client.post(
                "/predict",
                files={"file": ("dummy.jpg", img_bytes, "image/jpeg")}
            )
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("predicted_class", data)
            self.assertIn("confidence", data)
            self.assertIn("probabilities", data)
            self.assertIsInstance(data["confidence"], float)

    def test_predict_invalid_image_type(self):
        with TestClient(app) as client:
            response = client.post(
                "/predict",
                files={"file": ("dummy.txt", b"Hello World", "text/plain")}
            )
            self.assertEqual(response.status_code, 415)
            self.assertIn("Unsupported file format", response.json()["detail"])

    def test_predict_corrupt_image(self):
        with TestClient(app) as client:
            response = client.post(
                "/predict",
                files={"file": ("corrupt.jpg", b"This is not a real jpeg file content", "image/jpeg")}
            )
            self.assertEqual(response.status_code, 422)
            self.assertIn("Invalid or corrupt image data", response.json()["detail"])

    def test_predict_oversized_image(self):
        # Generate dummy bytes > 5MB
        big_bytes = b"0" * (6 * 1024 * 1024)
        with TestClient(app) as client:
            response = client.post(
                "/predict",
                files={"file": ("huge.jpg", big_bytes, "image/jpeg")}
            )
            self.assertEqual(response.status_code, 413)
            self.assertIn("File too large", response.json()["detail"])

if __name__ == "__main__":
    unittest.main()
