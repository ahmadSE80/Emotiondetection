import time
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import shared_data

# Load model
model = load_model("emotion_model.h5")

emotion_labels = [
    "Angry",
    "Disgust",
    "Fear",
    "Happy",
    "Neutral",
    "Sad",
    "Surprise"
]

emotion_scores = {
    "Happy": 100,
    "Surprise": 90,
    "Neutral": 70,
    "Sad": 30,
    "Angry": 20,
    "Fear": 10,
    "Disgust": 10
}

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

running = False


def start_detection():

    global running
    running = True

    cap = cv2.VideoCapture(0)

    while running:
        if shared_data.paused:
          continue

        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        faces = face_cascade.detectMultiScale(
            gray,
            1.3,
            5
        )

        students = []

        total_score = 0

        for i, (x, y, w, h) in enumerate(faces):

            roi = gray[y:y+h, x:x+w]

            roi = cv2.resize(
                roi,
                (48, 48)
            )

            roi = roi.astype("float32") / 255.0

            roi = np.expand_dims(
                roi,
                axis=0
            )

            roi = np.expand_dims(
                roi,
                axis=-1
            )

            prediction = model.predict(
                roi,
                verbose=0
            )

            emotion = emotion_labels[
                np.argmax(prediction)
            ]

            score = emotion_scores[
                emotion
            ]

            total_score += score

            if score >= 80:
                status = "Engaged"
            elif score >= 60:
                status = "Normal"
            else:
                status = "Low Focus"

            students.append(
                (
                    f"Student {i+1}",
                    emotion,
                    score,
                    status
                )
            )

            shared_data.emotion_counts[
                emotion
            ] += 1

            cv2.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                emotion,
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        shared_data.current_frame = frame.copy()

        shared_data.students = students

        if len(students) > 0:
            shared_data.engagement_score = int(
                total_score / len(students)
            )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    running = False


def stop_detection():
    global running
    running = False