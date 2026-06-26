import cv2
import numpy as np
import os


def save_image(image, folder="screenshots", filename=None):
    """Saves an image to the specified folder."""
    if not os.path.exists(folder):
        os.makedirs(folder)

    if filename is None:
        # Generate a unique filename with counter
        base = "capture"
        count = 1
        
        while os.path.exists(os.path.join(folder, f"{base}_{count}.jpg")):
            count += 1
        
        filename = f"{base}_{count}.jpg"

    filepath = os.path.join(folder, filename)
    cv2.imwrite(filepath, image)
    
    return filepath

def get_image_info(image):
    """Returns dimensions, channels, and size."""
    shape = image.shape

    if len(shape) == 2:
        height, width = shape
        channels = 1
    elif len(shape) == 3:
        height, width, channels = shape
    else:
        height, width = shape, shape
        channels = 1

    bytes_per_pixel = 1 if len(shape) == 2 else 3
    size_bytes = width * height * bytes_per_pixel
    size_kb = size_bytes / 1024

    return {
        "width": width,
        "height": height,
        "channels": channels,
        "size_kb": round(size_kb, 2)
    }