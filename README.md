# Face Analysis & Beauty Recommendation System

## Overview

The Face Analysis & Beauty Recommendation System is an AI-powered application that analyzes a user's facial features and provides personalized beauty recommendations.

The system uses:

* EfficientNet-B0 for Face Shape Classification
* MediaPipe Face Mesh for Facial Landmark Detection
* OpenCV for Image Processing
* Streamlit for Interactive User Interface

The application identifies facial characteristics such as face shape, eye shape, lip shape, nose shape, facial symmetry, and beauty score. Based on these features, it recommends suitable hairstyles, glasses, earrings, necklaces, and makeup styles.

---

## Features

### Face Shape Detection

Classifies faces into:

* Oval
* Round
* Square
* Heart
* Oblong

### Eye Analysis

Detects:

* Almond Eyes
* Round Eyes
* Eye Orientation

  * Upturned
  * Downturned
  * Neutral
* Eye Spacing

  * Close Set
  * Wide Set
* Hooded Eyes

### Lip Analysis

Detects:

* Thin Lips
* Balanced Lips
* Full Lips
* Heavy Upper Lips
* Heavy Lower Lips

### Nose Analysis

Detects:

* Narrow Nose
* Medium Nose
* Wide Nose

### Facial Symmetry

Calculates facial symmetry using facial landmark measurements.

### Beauty Score

Generates an overall beauty score based on:

* Facial Symmetry
* Face Shape
* Eye Shape
* Lip Shape
* Nose Shape

### Beauty Recommendations

Provides recommendations for:

* Hairstyles
* Glasses
* Earrings
* Necklaces
* Lipstick Shades
* Eyebrow Styles
* Eyeliner Styles

### Virtual Simulation

Applies:

* Lipstick Simulation
* Glasses Simulation

on the user's uploaded image.

---

## Technologies Used

### Programming Language

* Python

### Libraries

* OpenCV
* MediaPipe
* NumPy
* TensorFlow
* Keras
* Streamlit

### Deep Learning Model

* MobileNetV2

---

## Project Structure

FaceAnalysisProject/

├── uploads/

├── results/

├── assets/

│ ├── hairstyles/

│ ├── glasses/

│ ├── earrings/

│ ├── necklaces/

│ └── makeup/

├── models/

│ └── face_shape_model.h5

├── pages/

│ └── report.py

├── face_shape.py

├── face_features.py

├── recommendation.py

├── app.py

├── face_shape_result.txt

├── face_features_result.txt

├── beauty_score.txt

├── symmetry_result.txt

└── README.md

---

## Workflow

1. User uploads an image.
2. Face Shape is classified using MobileNetV2.
3. MediaPipe detects facial landmarks.
4. Eye, Lip, and Nose features are analyzed.
5. Facial Symmetry is calculated.
6. Beauty Score is generated.
7. Personalized beauty recommendations are produced.
8. Simulation results are generated.
9. Final Beauty Analysis Report is displayed.

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-repository.git
cd FaceAnalysisProject
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
streamlit run app.py
```

## Future Improvements

* Monolid Eye Detection using CNN
* Real-Time Webcam Analysis
* Advanced Makeup Simulation
* Skin Tone Detection
* AI Hairstyle Try-On
* 3D Face Analysis

## Authors

Final Year Project

Face Analysis & Beauty Recommendation System

Developed using Artificial Intelligence, Computer Vision, and Deep Learning.
