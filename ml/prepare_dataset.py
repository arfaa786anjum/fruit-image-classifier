"""
Fruits-360 Dataset Preparation Script
======================================
Downloads the Fruits-360 dataset via kagglehub, filters only
apple/banana/orange classes, splits into train/validation/test
(70/15/15), validates every image, and writes a data README.

Usage:
    python ml/prepare_dataset.py

Requirements:
    pip install kagglehub Pillow numpy scikit-learn
"""

import os
import sys
import shutil
import random
import pathlib
from collections import defaultdict

from PIL import Image

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SEED = 42
SPLIT_RATIOS = {"train": 0.70, "validation": 0.15, "test": 0.15}

# Class mapping: Fruits-360 folder name prefix → our class label
# Fruits-360 names apple varieties as "Apple Braeburn", "Apple Golden 1", etc.
# We merge all into "apple". Same logic for banana and orange.
CLASS_KEYWORDS = {
    "apple": "apple",
    "banana": "banana",
    "orange": "orange",
}

# Output directories (relative to this script's parent = ml/)
SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR / "data"
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def classify_folder(folder_name: str) -> str | None:
    """Map a Fruits-360 folder name to one of our three classes."""
    name_lower = folder_name.lower()
    for keyword, label in CLASS_KEYWORDS.items():
        if name_lower.startswith(keyword):
            return label
    return None


def validate_image(filepath: pathlib.Path) -> bool:
    """Return True if the file can be opened and verified as an image."""
    try:
        with Image.open(filepath) as img:
            img.verify()
        return True
    except Exception:
        return False


def collect_images(source_dir: pathlib.Path) -> dict[str, list[pathlib.Path]]:
    """
    Walk the source directory (Training + Test from Fruits-360),
    filter to our three classes, and return {class_label: [image_paths]}.
    """
    images: dict[str, list[pathlib.Path]] = defaultdict(list)

    if not source_dir.exists():
        print(f"ERROR: Source directory does not exist: {source_dir}")
        sys.exit(1)

    for class_dir in sorted(source_dir.iterdir()):
        if not class_dir.is_dir():
            continue
        label = classify_folder(class_dir.name)
        if label is None:
            continue  # skip classes we don't need

        for img_path in sorted(class_dir.iterdir()):
            if img_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                images[label].append(img_path)

    return dict(images)


def split_list(items: list, ratios: dict[str, float], seed: int) -> dict[str, list]:
    """Split a list into subsets according to ratios, with a fixed seed."""
    rng = random.Random(seed)
    shuffled = list(items)
    rng.shuffle(shuffled)

    n = len(shuffled)
    splits = {}
    start = 0
    keys = list(ratios.keys())

    for i, key in enumerate(keys):
        if i == len(keys) - 1:
            # Last split gets the remainder to avoid rounding loss
            splits[key] = shuffled[start:]
        else:
            count = round(n * ratios[key])
            splits[key] = shuffled[start : start + count]
            start += count

    return splits


def copy_images(
    splits: dict[str, list[pathlib.Path]],
    label: str,
    data_dir: pathlib.Path,
) -> dict[str, int]:
    """Copy images into data_dir/{split}/{label}/ and return counts."""
    counts = {}
    for split_name, paths in splits.items():
        dest = data_dir / split_name / label
        dest.mkdir(parents=True, exist_ok=True)
        for src in paths:
            shutil.copy2(src, dest / src.name)
        counts[split_name] = len(paths)
    return counts


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("Fruits-360 Dataset Preparation")
    print("=" * 60)

    # Step 1: Download via kagglehub
    print("\n[1/5] Downloading Fruits-360 dataset via kagglehub...")
    try:
        import kagglehub
    except ImportError:
        print("ERROR: kagglehub is not installed. Run: pip install kagglehub")
        sys.exit(1)

    dataset_path = pathlib.Path(kagglehub.dataset_download("moltean/fruits"))
    print(f"  Dataset downloaded to: {dataset_path}")

    # Step 2: Locate Training and Test directories
    print("\n[2/5] Locating source image directories...")

    # Fruits-360 structure: <path>/Training/ and <path>/Test/
    # Sometimes nested under a version folder
    training_dir = None
    test_dir = None

    for candidate in [dataset_path, *dataset_path.iterdir()]:
        if not candidate.is_dir():
            continue
        t = candidate / "Training"
        te = candidate / "Test"
        if t.exists() and te.exists():
            training_dir = t
            test_dir = te
            break

    # Also try lowercase variants
    if training_dir is None:
        for candidate in [dataset_path, *dataset_path.iterdir()]:
            if not candidate.is_dir():
                continue
            for child in candidate.iterdir():
                if child.is_dir() and child.name.lower() == "training":
                    training_dir = child
                if child.is_dir() and child.name.lower() == "test":
                    test_dir = child
            if training_dir and test_dir:
                break

    if training_dir is None or test_dir is None:
        print(f"ERROR: Could not find Training/Test directories in {dataset_path}")
        print("  Contents:", [p.name for p in dataset_path.iterdir()])
        sys.exit(1)

    print(f"  Training dir: {training_dir}")
    print(f"  Test dir:     {test_dir}")

    # Step 3: Collect and filter images
    print("\n[3/5] Collecting apple, banana, and orange images...")
    all_images: dict[str, list[pathlib.Path]] = defaultdict(list)

    for source_dir in [training_dir, test_dir]:
        partial = collect_images(source_dir)
        for label, paths in partial.items():
            all_images[label].extend(paths)

    # Report raw counts
    for label in sorted(all_images):
        print(f"  {label}: {len(all_images[label])} images found")

    if not all_images:
        print("ERROR: No matching images found!")
        sys.exit(1)

    # Validate we have all three classes
    for required in ["apple", "banana", "orange"]:
        if required not in all_images or len(all_images[required]) == 0:
            print(f"ERROR: No images found for class '{required}'")
            sys.exit(1)

    # Step 4: Validate images and split
    print("\n[4/5] Validating images and splitting 70/15/15 (seed=42)...")

    # Clear existing data splits (if re-running)
    for split_name in SPLIT_RATIOS:
        split_dir = DATA_DIR / split_name
        if split_dir.exists():
            shutil.rmtree(split_dir)

    total_valid = 0
    total_invalid = 0
    all_counts: dict[str, dict[str, int]] = {}

    for label in sorted(all_images):
        # Validate each image
        valid = []
        invalid = 0
        for img_path in all_images[label]:
            if validate_image(img_path):
                valid.append(img_path)
            else:
                invalid += 1
                print(f"  WARNING: Invalid image skipped: {img_path}")

        total_valid += len(valid)
        total_invalid += invalid

        # Split
        splits = split_list(valid, SPLIT_RATIOS, SEED)

        # Copy to output
        counts = copy_images(splits, label, DATA_DIR)
        all_counts[label] = counts

        print(f"  {label}: {len(valid)} valid ({invalid} invalid) → "
              f"train={counts['train']}, val={counts['validation']}, "
              f"test={counts['test']}")

    # Step 5: Write data README
    print("\n[5/5] Writing data README...")

    readme_path = DATA_DIR / "README.md"
    readme_path.parent.mkdir(parents=True, exist_ok=True)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("# Dataset — Fruit Image Classifier\n\n")
        f.write("## Source\n\n")
        f.write("- **Dataset:** Fruits-360\n")
        f.write("- **Kaggle ID:** `moltean/fruits`\n")
        f.write("- **Authors:** Horea Muresan, Mihai Oltean\n")
        f.write("- **License:** CC BY-SA 4.0 "
                "(Creative Commons Attribution-ShareAlike 4.0 International)\n")
        f.write("- **Citation:** Muresan & Oltean, \"Fruit recognition from images "
                "using deep learning,\" *Acta Univ. Sapientiae, Informatica*, "
                "Vol. 10, Issue 1, pp. 26-42, 2018\n")
        f.write(f"- **Image size:** 100×100 pixels\n")
        f.write(f"- **Format:** JPEG\n\n")
        f.write("## Classes\n\n")
        f.write("| Class | Description |\n")
        f.write("|---|---|\n")
        f.write("| `apple` | All apple varieties merged |\n")
        f.write("| `banana` | All banana varieties merged |\n")
        f.write("| `orange` | All orange varieties merged |\n\n")
        f.write("## Split\n\n")
        f.write(f"- **Random seed:** {SEED}\n")
        f.write("- **Strategy:** Stratified by class, shuffled, "
                "no duplicates across splits\n")
        f.write(f"- **Ratios:** train=70%, validation=15%, test=15%\n\n")
        f.write("| Class | Train | Validation | Test | Total |\n")
        f.write("|---|---|---|---|---|\n")

        grand_train = grand_val = grand_test = grand_total = 0
        for label in sorted(all_counts):
            c = all_counts[label]
            total = c["train"] + c["validation"] + c["test"]
            f.write(f"| {label} | {c['train']} | {c['validation']} "
                    f"| {c['test']} | {total} |\n")
            grand_train += c["train"]
            grand_val += c["validation"]
            grand_test += c["test"]
            grand_total += total

        f.write(f"| **Total** | **{grand_train}** | **{grand_val}** "
                f"| **{grand_test}** | **{grand_total}** |\n\n")

        if total_invalid > 0:
            f.write(f"**Note:** {total_invalid} invalid/corrupt images were "
                    f"skipped during preparation.\n")

    print(f"\n  Data README written to: {readme_path}")
    print(f"\n{'=' * 60}")
    print(f"DONE — {total_valid} valid images across 3 classes")
    print(f"  Invalid/skipped: {total_invalid}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
