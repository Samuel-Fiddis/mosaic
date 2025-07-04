from nearest_neighbour.nn import CIFAR_DATA, NNAlgorithm
import numpy as np
from io import BytesIO
from PIL import Image

from pprint import pprint

IMAGE_PIXEL_SIZE = 32


def load_image_to_array(image_data):
    # Open the image using PIL
    img = Image.open(BytesIO(image_data))

    # Convert to RGB if image is in a different mode (e.g., RGBA or grayscale)
    if img.mode != "RGB":
        img = img.convert("RGB")

    # Convert to numpy array
    img_array = np.array(img)

    return img_array


def process_image(image_array, algo: NNAlgorithm):
    x, y = image_array.shape[:2]
    x = x - (x % IMAGE_PIXEL_SIZE)  # Ensure dimensions are multiples of 32
    y = y - (y % IMAGE_PIXEL_SIZE)  # Ensure dimensions are multiples of 32
    print(x, y)
    new_image = np.zeros((x, y, 3), dtype=np.uint8)
    for i in range(0, x, IMAGE_PIXEL_SIZE):
        for j in range(0, y, IMAGE_PIXEL_SIZE):
            new_image[i : i + IMAGE_PIXEL_SIZE, j : j + IMAGE_PIXEL_SIZE] = algo.query(
                image_array[i : i + IMAGE_PIXEL_SIZE, j : j + IMAGE_PIXEL_SIZE]
            )
    new_image = Image.fromarray(new_image)
    img_byte_arr = BytesIO()
    new_image.save(img_byte_arr, format="PNG")
    return img_byte_arr.getvalue()
