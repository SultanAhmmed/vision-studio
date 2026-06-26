import cv2
import numpy as np


def track_color(image, color_name):
    """
    Tracks Red or Blue colors in HSV space.
    Returns the processed image with bounding boxes.
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    if color_name == "Red":
        lower = np.array([0, 50, 50])
        upper = np.array([10, 255, 255])
        # Red wraps around 180, so we need a second range
        lower2 = np.array([160, 50, 50])
        upper2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower, upper)
        mask2 = cv2.inRange(hsv, lower2, upper2)
        mask = cv2.bitwise_or(mask1, mask2)

    elif color_name == "Blue":
        lower = np.array([100, 50, 50])
        upper = np.array([130, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)
    
    else:
        return image, None
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    output = image.copy()
    detected = False

    for contour in contours:
        if cv2.contourArea(contour) > 500: # Ignore small noise
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(output, (x,y), (x+w, y+h), (0, 255, 0), 2)
            detected = True

    return output, detected

def detect_motion(current_frame, previous_frame):
    """
    Calculates motion between two frames.
    Returns: (processed_frame, motion_detected_bool)
    """
    if previous_frame is None:
        return current_frame, False
    
    # Calculate absolute difference
    delta = cv2.absdiff(previous_frame, current_frame)
    gray = cv2.cvtColor(delta, cv2.COLOR_BGR2GRAY)

    # Threshold to get binary motion map
    _, thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)

    # Morphological operations to fill holes
    thresh = cv2.dilate(thresh, None, iterations=2)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    output = current_frame.copy()
    motion_detected = False

    for contour in contours:
        if cv2.contourArea(contour) > 1000: # Filter small noise
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(output, (x,y), (x+w, y+h), (0, 255, 0), 2)
            motion_detected = True
    
    return output, motion_detected


