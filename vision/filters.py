import cv2
import numpy as np


def apply_grayscale(image):
    """Converts to grayscale if not already."""
    if len(image.shape) == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image


def apply_blur(image, kernel_size=(11, 11)):
    """Applies Gaussian Blur (works on both grayscale and color)."""
    # Ensure kernel size is odd by checking tuple elements
    k_w, k_h = kernel_size
    if k_w % 2 == 0:
        k_w += 1
    if k_h % 2 == 0:
        k_h += 1

    kernel_size = (k_w, k_h)

    # OpenCV blur works on both 1-channel and 3-channel images
    return cv2.GaussianBlur(image, kernel_size, 0)


def apply_sharpen(image):
    """Applies sharpening (works on both grayscale and color)."""
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    return cv2.filter2D(image, -1, kernel)


def apply_sepia(image):
    """Applies Sepia filter. Converts grayscale to color if necessary."""
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    sepia_filter = np.array(
        [[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]],
        dtype=np.float32,
    )

    sepia_image = cv2.transform(image, sepia_filter)
    return np.clip(sepia_image, 0, 255).astype("uint8")


def apply_edge_detection(image):
    """Detects edges (works on both grayscale and color)."""
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    return cv2.Canny(blur, 100, 200)
