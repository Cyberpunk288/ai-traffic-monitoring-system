import os
import random
import shutil

# ==========================
# Configuration
# ==========================

IMAGE_DIR = "images"
LABEL_DIR = "labels"
OUTPUT_DIR = "dataset"

TRAIN_RATIO = 0.70
VAL_RATIO = 0.20
TEST_RATIO = 0.10

RANDOM_SEED = 42


# ==========================
# Check ratios
# ==========================

if abs(TRAIN_RATIO + VAL_RATIO + TEST_RATIO - 1.0) > 1e-9:
    raise ValueError("Train, validation, and test ratios must add up to 1.0")


# ==========================
# Get images
# ==========================

images = [
    f for f in os.listdir(IMAGE_DIR)
    if f.lower().endswith(".jpg")
]

print("========================================")
print("DATASET SPLITTING")
print("========================================")
print(f"Total images: {len(images)}")


# ==========================
# Make sure every image has
# a corresponding label
# ==========================

valid_images = []

for image_name in images:

    label_name = os.path.splitext(image_name)[0] + ".txt"

    label_path = os.path.join(LABEL_DIR, label_name)

    if os.path.exists(label_path):
        valid_images.append(image_name)

    else:
        print(f"Missing label: {image_name}")


print(f"Images with labels: {len(valid_images)}")


# ==========================
# Shuffle reproducibly
# ==========================

random.seed(RANDOM_SEED)

random.shuffle(valid_images)


# ==========================
# Calculate split sizes
# ==========================

total = len(valid_images)

train_count = int(total * TRAIN_RATIO)
val_count = int(total * VAL_RATIO)

train_images = valid_images[:train_count]

val_images = valid_images[
    train_count:train_count + val_count
]

test_images = valid_images[
    train_count + val_count:
]


# ==========================
# Create directories
# ==========================

splits = {
    "train": train_images,
    "val": val_images,
    "test": test_images
}

for split in splits:

    os.makedirs(
        os.path.join(OUTPUT_DIR, "images", split),
        exist_ok=True
    )

    os.makedirs(
        os.path.join(OUTPUT_DIR, "labels", split),
        exist_ok=True
    )


# ==========================
# Copy images and labels
# ==========================

for split, image_list in splits.items():

    print(f"\nCopying {split} data: {len(image_list)} images")

    for image_name in image_list:

        label_name = (
            os.path.splitext(image_name)[0]
            + ".txt"
        )

        source_image = os.path.join(
            IMAGE_DIR,
            image_name
        )

        source_label = os.path.join(
            LABEL_DIR,
            label_name
        )

        destination_image = os.path.join(
            OUTPUT_DIR,
            "images",
            split,
            image_name
        )

        destination_label = os.path.join(
            OUTPUT_DIR,
            "labels",
            split,
            label_name
        )

        shutil.copy2(
            source_image,
            destination_image
        )

        shutil.copy2(
            source_label,
            destination_label
        )


# ==========================
# Final report
# ==========================

print("\n========================================")
print("DATASET SPLIT COMPLETE")
print("========================================")

print(f"Training images:   {len(train_images)}")
print(f"Validation images: {len(val_images)}")
print(f"Testing images:    {len(test_images)}")

print("----------------------------------------")

print(
    f"Total: {len(train_images) + len(val_images) + len(test_images)}"
)

print("========================================")