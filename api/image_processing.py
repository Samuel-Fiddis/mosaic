from concurrent.futures import ThreadPoolExecutor
from io import BytesIO

import numpy as np
from nearest_neighbour.nn import NNAlgorithm
from PIL import Image

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



def _process_block(args):
    i, j, block, algo = args
    return (i, j, algo.query(block))

def process_image(image_array, algo: NNAlgorithm):
    x, y = image_array.shape[:2]
    x = x - (x % IMAGE_PIXEL_SIZE)  # Ensure dimensions are multiples of 32
    y = y - (y % IMAGE_PIXEL_SIZE)  # Ensure dimensions are multiples of 32
    new_image = np.zeros((x, y, 3), dtype=np.uint8)

    tasks = []
    for i in range(0, x, IMAGE_PIXEL_SIZE):
        for j in range(0, y, IMAGE_PIXEL_SIZE):
            block = image_array[i : i + IMAGE_PIXEL_SIZE, j : j + IMAGE_PIXEL_SIZE]
            tasks.append((i, j, block, algo))

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(_process_block, tasks))

    for i, j, processed_block in results:
        new_image[i : i + IMAGE_PIXEL_SIZE, j : j + IMAGE_PIXEL_SIZE] = processed_block

    new_image = Image.fromarray(new_image)
    img_byte_arr = BytesIO()
    new_image.save(img_byte_arr, format="PNG")
    return img_byte_arr.getvalue()
