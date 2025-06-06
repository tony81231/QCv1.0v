# qc_logic.py

import numpy as np
import cv2

def assess_white_balance(image):
    """Check if image is properly white balanced."""
    mean_color = np.mean(image, axis=(0, 1))
    red, green, blue = mean_color
    deviation = abs(red - green) + abs(green - blue) + abs(red - blue)
    if deviation > 40:  # Threshold can be adjusted based on real data
        return False, "White Balance Adjustment Needed"
    return True, ""

def assess_highlight_clipping(image, ignore_lamps=False):
    """Detect highlight clipping and optionally ignore ceiling lights."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, clipped_mask = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY)
    clipping_percentage = np.sum(clipped_mask) / (gray.shape[0] * gray.shape[1] * 255) * 100

    if clipping_percentage > 2.0:  # 2% threshold
        if ignore_lamps:
            return True, "Highlight Clipping Detected from Lamps (Fair)"
        return False, "Highlight Clipping Detected"
    return True, ""

def assess_contrast(image):
    """Check if image has balanced contrast."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    std_dev = np.std(gray)
    if std_dev < 30:
        return False, "Increase Image Contrast"
    return True, ""

def assess_hdr_image(image, ignore_lamps=False):
    """
    Assess HDR image based on multiple quality checks.
    Returns: score (int), label (str), corrections (list of str)
    """
    score = 10
    comments = []

    checks = [
        assess_white_balance(image),
        assess_highlight_clipping(image, ignore_lamps),
        assess_contrast(image)
        # Add more checks here (sharpness, straightening, etc.)
    ]

    for passed, comment in checks:
        if not passed:
            score -= 2
            comments.append(comment)

    # Clamp score
    score = max(4, score)

    # Map score to label
    if score >= 9:
        label = "Excellent"
    elif score >= 7:
        label = "Good"
    elif score >= 5:
        label = "Fair"
    else:
        label = "Poor"

    return score, label, comments
