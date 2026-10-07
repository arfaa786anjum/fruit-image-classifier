import os
import pathlib
import random
from PIL import Image, ImageDraw

# Configuration
SEED = 42
CLASSES = {
    "apple": (220, 20, 20),      # Red
    "banana": (240, 230, 20),    # Yellow
    "orange": (240, 130, 20)     # Orange
}
COUNTS = {"train": 70, "validation": 15, "test": 15}
IMG_SIZE = (100, 100)

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR / "data"

def generate_mock_image(color, path):
    # Base color with some random noise
    img = Image.new("RGB", IMG_SIZE, color)
    draw = ImageDraw.Draw(img)
    # Add some random noise dots
    for _ in range(500):
        x = random.randint(0, IMG_SIZE[0]-1)
        y = random.randint(0, IMG_SIZE[1]-1)
        noise_color = (
            min(255, max(0, color[0] + random.randint(-30, 30))),
            min(255, max(0, color[1] + random.randint(-30, 30))),
            min(255, max(0, color[2] + random.randint(-30, 30)))
        )
        draw.point((x, y), fill=noise_color)
    img.save(path)

def main():
    print("=" * 60)
    print("Generating Mock Dataset")
    print("=" * 60)
    
    random.seed(SEED)
    
    # Clear existing
    if DATA_DIR.exists():
        import shutil
        shutil.rmtree(DATA_DIR)
        
    total_images = 0
    for class_name, color in CLASSES.items():
        print(f"\nProcessing {class_name}...")
        for split, count in COUNTS.items():
            split_dir = DATA_DIR / split / class_name
            split_dir.mkdir(parents=True, exist_ok=True)
            for i in range(count):
                img_path = split_dir / f"{class_name}_{split}_{i}.jpg"
                generate_mock_image(color, img_path)
                total_images += 1
            print(f"  {split}: {count} images")

    # Write README
    readme_path = DATA_DIR / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("# Dataset — Fruit Image Classifier (Mock)\n\n")
        f.write("## Source\n\n")
        f.write("- **Dataset:** Generated mock dataset for rapid prototyping\n")
        f.write(f"- **Image size:** {IMG_SIZE[0]}x{IMG_SIZE[1]} pixels\n")
        f.write("- **Format:** JPEG\n\n")
        f.write("## Classes\n\n")
        for cls in CLASSES:
            f.write(f"- `{cls}`\n")
        f.write("\n## Split\n\n")
        f.write(f"- **train:** {COUNTS['train']}/class\n")
        f.write(f"- **validation:** {COUNTS['validation']}/class\n")
        f.write(f"- **test:** {COUNTS['test']}/class\n")

    print(f"\nDONE — {total_images} total mock images generated in ml/data/")

if __name__ == "__main__":
    main()
