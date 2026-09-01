import cv2
import os

IMAGE_DIR = "images"

images = [
    f for f in os.listdir(IMAGE_DIR)
    if f.lower().endswith(".jpg")
]

below_320 = 0
between_320_640 = 0
above_640 = 0

print("========================================")
print("IMAGE SIZE ANALYSIS")
print("========================================")
print(f"Total images: {len(images)}")
print()

for image_name in images:

    image_path = os.path.join(IMAGE_DIR, image_name)

    image = cv2.imread(image_path)

    if image is None:
        continue

    height, width = image.shape[:2]

    shortest_side = min(width, height)

    if shortest_side < 320:
        below_320 += 1

    elif shortest_side < 640:
        between_320_640 += 1

    else:
        above_640 += 1

print("----------------------------------------")
print(f"Shortest side < 320 px: {below_320}")
print(f"Shortest side 320-639 px: {between_320_640}")
print(f"Shortest side >= 640 px: {above_640}")
print("========================================")