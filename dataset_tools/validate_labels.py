import os

IMAGE_DIR = "images"
LABEL_DIR = "labels"

# Get all images and labels
images = [
    f for f in os.listdir(IMAGE_DIR)
    if f.lower().endswith(".jpg")
]

labels = [
    f for f in os.listdir(LABEL_DIR)
    if f.lower().endswith(".txt")
]

image_basenames = {
    os.path.splitext(f)[0]
    for f in images
}

label_basenames = {
    os.path.splitext(f)[0]
    for f in labels
}

print("========================================")
print("YOLO DATASET VALIDATION")
print("========================================")

print(f"Total images: {len(images)}")
print(f"Total labels: {len(labels)}")

# Check missing labels
missing_labels = image_basenames - label_basenames

# Check labels without images
missing_images = label_basenames - image_basenames

print(f"Missing labels: {len(missing_labels)}")
print(f"Labels without images: {len(missing_images)}")

# Validation counters
valid_lines = 0
invalid_lines = 0
invalid_class = 0
invalid_coordinates = 0
empty_labels = 0

# Check every label file
for label_file in labels:

    label_path = os.path.join(LABEL_DIR, label_file)

    with open(label_path, "r") as file:
        lines = file.readlines()

    if len(lines) == 0:
        empty_labels += 1
        continue

    for line in lines:

        parts = line.strip().split()

        # YOLO annotation must contain 5 values
        if len(parts) != 5:
            invalid_lines += 1
            continue

        try:
            class_id = int(parts[0])
            x_center = float(parts[1])
            y_center = float(parts[2])
            box_width = float(parts[3])
            box_height = float(parts[4])

        except ValueError:
            invalid_lines += 1
            continue

        # We expect class 0
        if class_id != 0:
            invalid_class += 1

        # YOLO coordinates must be between 0 and 1
        if not (
            0 <= x_center <= 1
            and 0 <= y_center <= 1
            and 0 < box_width <= 1
            and 0 < box_height <= 1
        ):
            invalid_coordinates += 1
        else:
            valid_lines += 1


print("----------------------------------------")
print(f"Valid annotation lines: {valid_lines}")
print(f"Invalid annotation lines: {invalid_lines}")
print(f"Invalid class IDs: {invalid_class}")
print(f"Invalid coordinates: {invalid_coordinates}")
print(f"Empty label files: {empty_labels}")
print("========================================")