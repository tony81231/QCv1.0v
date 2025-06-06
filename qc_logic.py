# qc_logic.py

import numpy as np
import cv2

def assess_white_balance(image):
    mean_color = np.mean(image, axis=(0, 1))
    red, green, blue = mean_color
    deviation = abs(red - green) + abs(green - blue) + abs(red - blue)
    if deviation > 40:
        return False, "White Balance Adjustment Needed"
    return True, ""

def assess_highlight_clipping(image, ignore_lamps=False):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, clipped_mask = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY)
    clipping_percentage = np.sum(clipped_mask) / (gray.shape[0] * gray.shape[1] * 255) * 100
    if clipping_percentage > 2.0:
        if ignore_lamps:
            return True, "Highlight Clipping Detected from Lamps (Fair)"
        return False, "Highlight Clipping Detected"
    return True, ""

def assess_contrast(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    std_dev = np.std(gray)
    if std_dev < 30:
        return False, "Increase Image Contrast"
    return True, ""

def assess_hdr_image(image, ignore_lamps=False):
    score = 10
    comments = []

    checks = [
        assess_white_balance(image),
        assess_highlight_clipping(image, ignore_lamps),
        assess_contrast(image)
    ]

    for passed, comment in checks:
        if not passed:
            score -= 2
            comments.append(comment)

    score = max(4, score)

    if score >= 9:
        label = "Excellent"
    elif score >= 7:
        label = "Good"
    elif score >= 5:
        label = "Fair"
    else:
        label = "Poor"

    return score, label, comments
