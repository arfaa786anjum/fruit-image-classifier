import os
import unittest
import pathlib
import numpy as np
from PIL import Image

# Import the predictor
# Note: we run this using `python -m unittest discover -s ml/tests` from the project root
import sys
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))
from predict import FruitPredictor

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent

class TestMLPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a dummy image for testing
        cls.test_img_path = SCRIPT_DIR / "dummy.jpg"
        img = Image.new("RGB", (200, 200), color=(255, 0, 0))
        img.save(cls.test_img_path)
        
        cls.predictor = FruitPredictor()
        try:
            cls.predictor.load_model()
            cls.model_loaded = True
        except Exception:
            cls.model_loaded = False
            
    @classmethod
    def tearDownClass(cls):
        if cls.test_img_path.exists():
            os.remove(cls.test_img_path)

    def test_image_loading_and_preprocessing_dimensions(self):
        if not self.model_loaded:
            self.skipTest("Model not loaded. Train model first.")
            
        img_size = tuple(self.predictor.metadata["img_size"])
        img = Image.open(self.test_img_path).convert("RGB")
        img = img.resize(img_size)
        img_array = np.array(img) / 255.0
        
        self.assertEqual(img_array.shape, (img_size[0], img_size[1], 3), "Image preprocessing dimensions mismatch")

    def test_class_mapping(self):
        if not self.model_loaded:
            self.skipTest("Model not loaded. Train model first.")
            
        mapping = self.predictor.class_mapping
        self.assertIn("apple", mapping.values())
        self.assertIn("banana", mapping.values())
        self.assertIn("orange", mapping.values())

    def test_prediction_output(self):
        if not self.model_loaded:
            self.skipTest("Model not loaded. Train model first.")
            
        res = self.predictor.predict_image(str(self.test_img_path))
        self.assertIn("predicted_class", res)
        self.assertIn("confidence", res)
        self.assertIn("probabilities", res)
        
        self.assertIn(res["predicted_class"], self.predictor.class_mapping.values())
        self.assertTrue(0.0 <= res["confidence"] <= 1.0)
        self.assertEqual(len(res["probabilities"]), len(self.predictor.class_mapping))

if __name__ == "__main__":
    unittest.main()
