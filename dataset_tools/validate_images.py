import cv2
import os

IMAGE_DIR = "images"

images = [
    f for f in os.listdir(IMAGE_DIR)
    if f.lower().endswith(".jpg")
]

valid_images = 0
corrupted_images = 0

widths = []
heights = []

print("========================================")
print("IMAGE DATASET VALIDATION")
print("========================================")
print(f"Total images: {len(images)}")
print()

for image_name in images:

    image_path = os.path.join(IMAGE_DIR, image_name)

    image = cv2.imread(image_path)

    if image is None:
        print(f"Could not read: {image_name}")
        corrupted_images += 1
        continue

    height, width = image.shape[:2]

    widths.append(width)
    heights.append(height)

    valid_images += 1


print("----------------------------------------")
print(f"Valid images: {valid_images}")
print(f"Corrupted/unreadable images: {corrupted_images}")

if widths and heights:

    print("----------------------------------------")
    print(f"Minimum width: {min(widths)}")
    print(f"Maximum width: {max(widths)}")
    print(f"Minimum height: {min(heights)}")
    print(f"Maximum height: {max(heights)}")

    print("----------------------------------------")

    unique_resolutions = set(
        zip(widths, heights)
    )

    print(f"Unique resolutions: {len(unique_resolutions)}")

print("========================================")