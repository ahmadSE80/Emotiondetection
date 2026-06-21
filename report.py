import streamlit as st

with open("face_shape_result.txt", "r") as f:
    predicted_class = f.read().strip()

with open("face_features_result.txt", "r") as f:
    lines = f.readlines()

eye_type = lines[0].strip()
lip_type = lines[1].strip()
nose_type = lines[2].strip()

st.title("📊 Beauty Analysis Report")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Overall Score",
        "87/100"
    )

with col2:
    st.metric(
        "Facial Symmetry",
        "85%"
    )

with col3:
    st.metric(
        "Visual Age",
        "20"
    )

st.subheader("Face Features")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.info(f"Face Shape\n\n{predicted_class}")

with c2:
    st.info(f"Lip Shape\n\n{lip_type}")

with c3:
    st.info(f"Nose Shape\n\n{nose_type}")

with c4:
    st.info(f"Eye Shape\n\n{eye_type}")
    
st.subheader("👓 Glasses Recommendation")

st.image(
    "assets/glasses/round_glass.png",
    width=300
)

st.write("Recommended: Round Frame")

st.subheader("💄 Makeup Recommendation")

c1, c2, c3 = st.columns(3)

with c1:
    st.write("Lipstick")
    st.success("Maroon")

with c2:
    st.write("Eyebrow")
    st.success("Soft Brow")

with c3:
    st.write("Eyeliner")
    st.success("Thin Wing")

st.subheader("💍 Jewelry Recommendation")

c1, c2 = st.columns(2)

with c1:
    st.write("Necklace")
    st.success("Minimal Pendant")

with c2:
    st.write("Earrings")
    st.success("Round Earrings")

