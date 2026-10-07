import os
import json
import pathlib
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR / "data"
MODELS_DIR = SCRIPT_DIR / "models"
REPORTS_DIR = SCRIPT_DIR / "reports"

def main():
    print("=" * 60)
    print("Model Evaluation - Phase 2")
    print("=" * 60)
    
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    model_path = MODELS_DIR / "fruit_classifier.keras"
    metadata_path = MODELS_DIR / "metadata.json"
    
    if not model_path.exists() or not metadata_path.exists():
        print("Model or metadata not found. Please run train.py first.")
        return
        
    with open(metadata_path, "r") as f:
        metadata = json.load(f)
        
    img_size = tuple(metadata["img_size"])
    class_mapping = {int(k): v for k, v in metadata["class_mapping"].items()}
    class_names = [class_mapping[i] for i in range(len(class_mapping))]
    
    # Load model
    model = tf.keras.models.load_model(model_path)
    
    test_datagen = ImageDataGenerator(rescale=1./255)
    test_generator = test_datagen.flow_from_directory(
        DATA_DIR / "test",
        target_size=img_size,
        batch_size=32,
        class_mode='categorical',
        shuffle=False
    )
    
    print("\nEvaluating on test set...")
    loss, accuracy = model.evaluate(test_generator)
    print(f"Test Loss: {loss:.4f}")
    print(f"Test Accuracy: {accuracy:.4f}")
    
    print("\nGenerating predictions for classification report and confusion matrix...")
    predictions = model.predict(test_generator)
    y_pred = np.argmax(predictions, axis=1)
    y_true = test_generator.classes
    
    report = classification_report(y_true, y_pred, target_names=class_names)
    cm = confusion_matrix(y_true, y_pred)
    
    print("\nClassification Report:")
    print(report)
    print("Confusion Matrix:")
    print(cm)
    
    # Save report
    report_file = REPORTS_DIR / "evaluation_report.txt"
    with open(report_file, "w") as f:
        f.write(f"Test Accuracy: {accuracy:.4f}\n")
        f.write(f"Test Loss: {loss:.4f}\n\n")
        f.write("Classification Report:\n")
        f.write(report)
        f.write("\nConfusion Matrix:\n")
        f.write(str(cm))
        f.write("\n\nLimitations:\n")
        f.write("- The model was trained on a very small mock dataset (for prototyping) and may not generalize to real images.\n")
        f.write("- Overfitting is possible due to the limited number of diverse samples in the dataset.\n")
    print(f"\nReport saved to {report_file}")

if __name__ == "__main__":
    main()
