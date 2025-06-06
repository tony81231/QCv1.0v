# app.py

import streamlit as st
import numpy as np
import cv2
from qc_logic import assess_hdr_image

def load_image(uploaded_file):
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    return cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

st.set_page_config(page_title="HDR QC Assistant", layout="centered")

st.title("📸 HDR QC Assistant")
st.caption("Upload a processed HDR image for automated QC assessment based on BoxBrownie's guide.")

uploaded_file = st.file_uploader("Upload HDR Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = load_image(uploaded_file)
    st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption="Preview", use_column_width=True)

    st.divider()

    st.subheader("QC Settings")
    ignore_lamps = st.checkbox("Ignore highlight clipping from ceiling lights?", value=False)

    if st.button("Run QC Assessment"):
        score, label, corrections = assess_hdr_image(image, ignore_lamps)

        st.subheader("QC Results")
        st.markdown(f"**Score:** {score}/10")
        st.markdown(f"**Rating:** {label}")

        st.divider()

        st.subheader("Corrections Needed")
        if corrections:
            for c in corrections:
                st.markdown(f"- {c}")
        else:
            st.markdown("✅ No corrections needed!")

    st.info("QC results are based on BoxBrownie's 16-step process and our AI-enhanced highlight detection.")
else:
    st.warning("Please upload an HDR image to begin QC assessment.")
