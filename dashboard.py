import streamlit as st
from PIL import Image
import subprocess

st.set_page_config(
    page_title="AI Beauty Analyzer",
    layout="wide"
)

# Centered Title
st.markdown(
    """
    <h1 style='text-align:center;'>
        💄 AI Beauty Analyzer
    </h1>
    <p style='text-align:center; font-size:20px;'>
        Discover your Face Shape, Eyes, Nose, Lips and Beauty Features
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# Two Columns
col1, col2 = st.columns([1,1])

with col1:
    st.image(
        "assets/girl.jpg",   # your girl image
        use_container_width=True
    )

with col2:

    uploaded_file = st.file_uploader(
        "Upload Your Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        img = Image.open(uploaded_file)
        img.save("uploads/user.jpg")

        st.success("Image Uploaded Successfully")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔍 Analyze Face"):

        with st.spinner("Analyzing your face... Please wait ⏳"):

            result = subprocess.run(
                [r"D:\FaceAnalysisProject\venv\Scripts\python.exe",
             "predict_face_shape.py"]
        )

            result2 = subprocess.run(
                [r"D:\FaceAnalysisProject\venv\Scripts\python.exe",
             "face_features.py"]
        )

        if result.returncode == 0 and result2.returncode == 0:
            st.success("Analysis Complete ✅")
            st.switch_page("pages/report.py")
        else:
            st.error("Analysis Failed ❌")


st.markdown(
    "<h2 style='text-align:center;'>What We Analyze</h2>",
    unsafe_allow_html=True
)

# Row 1
c1, c2, c3 = st.columns(3)

with c1:
    st.info("🧑 Face Shape\n\nHeart, Oval, Round, Square, Oblong")

with c2:
    st.info("👁 Eye Shape\n\nAlmond, Round, Hooded, Upturned")

with c3:
    st.info("👃 Nose Shape\n\nAnalyze nose structure and type")

# Row 2
c4, c5, c6 = st.columns(3)

with c4:
    st.info("👄 Lip Shape\n\n\n\nFull, Thin, Wide and more")

with c5:
    st.info("💇 Hairstyle\n\nPersonalized hairstyle recommendation")

with c6:
    st.info("✨ Beauty Report\n\nComplete facial feature analysis")