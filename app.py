# app.py

import streamlit as st
import numpy as np
import cv2
from qc_logic import assess_hdr_image

def load_image(uploaded_file):
    """Convert uploaded file to OpenCV image."""
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    return cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

st.set_page_config(page_title="HDR QC Assistant", layout="centered")
st.title("🏠 HDR QC Assistant")

uploaded_file = st.file_uploader("Upload a final HDR image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = load_image(uploaded_file)
    st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption="Uploaded Image", use_column_width=True)

    ignore_lamps = st.checkbox("Ignore highlight clipping from ceiling lights?", value=False)

    if st.button("Run QC Assessment"):
        score, label, comments = assess_hdr_image(image, ignore_lamps)
        st.subheader(f"Score: {score}/10 - {label}")
        if comments:
            st.markdown("**Corrections Suggested:**")
            for c in comments:
                st.markdown(f"- {c}")
        else:
            st.markdown("✅ No corrections needed!")
