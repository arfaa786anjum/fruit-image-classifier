import os
import json
import random
import pathlib
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, callbacks
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Configuration
SEED = 42
IMG_SIZE = (128, 128)
BATCH_SIZE = 32
EPOCHS = 15
SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR / "data"
MODELS_DIR = SCRIPT_DIR / "models"

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)

def build_model(num_classes):
    model = models.Sequential([
        layers.Input(shape=(IMG_SIZE[0], IMG_SIZE[1], 3)),
        layers.Conv2D(32, (3, 3), activation='relu'),
        layers.MaxPooling2D(2, 2),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D(2, 2),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

def main():
    print("=" * 60)
    print("CNN Training - Phase 2")
    print("=" * 60)
    set_seed(SEED)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Data Augmentation & Normalization
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    train_generator = train_datagen.flow_from_directory(
        DATA_DIR / "train",
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        seed=SEED
    )
    
    val_generator = val_datagen.flow_from_directory(
        DATA_DIR / "validation",
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )
    
    # Save class mapping
    class_indices = train_generator.class_indices
    class_mapping = {v: k for k, v in class_indices.items()}
    metadata = {
        "class_mapping": class_mapping,
        "img_size": IMG_SIZE,
        "seed": SEED,
        "preprocessing": "rescale=1./255"
    }
    with open(MODELS_DIR / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)
    print(f"Class mapping: {class_mapping}")
    
    model = build_model(num_classes=len(class_indices))
    model.summary()
    
    # Early stopping and model checkpoint
    model_path = MODELS_DIR / "fruit_classifier.keras"
    early_stopping = callbacks.EarlyStopping(
        monitor='val_loss',
        patience=3,
        restore_best_weights=True
    )
    checkpoint = callbacks.ModelCheckpoint(
        filepath=str(model_path),
        monitor='val_loss',
        save_best_only=True
    )
    
    print("\nStarting training...")
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=val_generator,
        callbacks=[early_stopping, checkpoint]
    )
    
    model.save(model_path)
    print(f"\nTraining complete. Model saved to {model_path}")
    print(f"Metadata saved to {MODELS_DIR / 'metadata.json'}")

if __name__ == "__main__":
    main()
