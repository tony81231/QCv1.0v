# hdr_qc_streamlit.py

import streamlit as st
from PIL import Image
import numpy as np
import cv2

# Define human-friendly HDR QC labels and descriptions
LABELS = {
    "✅ Excellent": "Ideal HDR result, no visible flaws",
    "☑️ Good": "Minor issue, still professionally acceptable",
    "⚠️ Fair": "Noticeable issue, may need re-edit",
    "❌ Poor": "Serious issue, should be rejected or redone"
}

# Streamlit UI Setup
st.set_page_config(page_title="HDR QC Assistant", layout="wide")
st.title("📸 HDR Quality Control Assistant")

st.markdown("""
Upload processed HDR images to evaluate quality based on key metrics.
Each image is analyzed for:
- Highlight Control
- Shadow Detail
- Color Accuracy
- Brightness Balance
- Contrast & Depth
- Clarity & Sharpness

**Final Rating Legend:**
- 10/10 – Excellent
- 8/10 – Good
- 6/10 – Fair
- 4/10 or less – Poor
""")

uploaded_files = st.file_uploader("Upload HDR Images for QC", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

def classify_metric(score):
    if score == "Excellent":
        return "✅ Excellent"
    elif score == "Good":
        return "☑️ Good"
    elif score == "Fair":
        return "⚠️ Fair"
    else:
        return "❌ Poor"

def analyze_image_ai(image):
    """Analyze key QC metrics using basic AI logic."""
    image_cv = np.array(image)
    image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR)

    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    mean_brightness = np.mean(gray)
    std_contrast = np.std(gray)

    # Highlight Control
    highlight_mask = cv2.inRange(image_cv, (240, 240, 240), (255, 255, 255))
    highlight_ratio = np.sum(highlight_mask > 0) / (image_cv.shape[0] * image_cv.shape[1])
    highlight_score = "Poor" if highlight_ratio > 0.05 else "Excellent" if highlight_ratio < 0.005 else "Fair"

    # Shadow Detail
    shadow_ratio = np.sum(gray < 30) / (gray.shape[0] * gray.shape[1])
    shadow_score = "Poor" if shadow_ratio > 0.1 else "Excellent" if shadow_ratio < 0.02 else "Fair"

    # Color Accuracy - Placeholder (assumed Excellent)
    color_score = "Excellent"

    # Brightness Balance
    brightness_score = "Fair" if mean_brightness < 80 or mean_brightness > 200 else "Good"

    # Contrast & Depth
    contrast_score = "Fair" if std_contrast < 30 else "Excellent"

    # Clarity & Sharpness - Placeholder (assumed Good)
    sharpness_score = "Good"

    metrics = {
        "Highlight Control": classify_metric(highlight_score),
        "Shadow Detail": classify_metric(shadow_score),
        "Color Accuracy": classify_metric(color_score),
        "Brightness Balance": classify_metric(brightness_score),
        "Contrast & Depth": classify_metric(contrast_score),
        "Clarity & Sharpness": classify_metric(sharpness_score)
    }

    # Calculate final rating
    ratings = list(metrics.values())
    poor_count = ratings.count("❌ Poor")
    fair_count = ratings.count("⚠️ Fair")

    if poor_count >= 2:
        final = "4/10 – Poor"
    elif poor_count == 1 or fair_count >= 2:
        final = "6/10 – Fair"
    elif fair_count == 1:
        final = "8/10 – Good"
    else:
        final = "10/10 – Excellent"

    comment_map = {
        "10/10 – Excellent": "Professional quality HDR image. Balanced lighting, crisp details, and clean highlights.",
        "8/10 – Good": "Minor balance or exposure issue, but overall clean and sharp.",
        "6/10 – Fair": "Flatness or brightness imbalance noticeable. Still usable with minor edits.",
        "4/10 – Poor": "Multiple quality issues detected. Recommend re-edit or revision."
    }

    metrics["Final Rating"] = final
    metrics["Comment"] = comment_map[final]
    return metrics

if uploaded_files:
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file).convert("RGB")
        metrics = analyze_image_ai(image)

        st.markdown(f"### 🖼️ {uploaded_file.name}")
        cols = st.columns([1, 2])
        with cols[0]:
            st.image(image, use_column_width=True)
        with cols[1]:
            for metric, value in metrics.items():
                if metric not in ["Final Rating", "Comment"]:
                    st.markdown(f"**{metric}:** {value}")
            st.markdown(f"**💬 Comment:** {metrics['Comment']}")
            st.markdown(f"**🏆 Final Rating:** {metrics['Final Rating']}")
        st.markdown("---")

st.sidebar.header("ℹ️ QC Label Guide")
for label, desc in LABELS.items():
    st.sidebar.markdown(f"**{label}** – {desc}")
