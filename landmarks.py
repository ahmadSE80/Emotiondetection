import cv2
import mediapipe as mp

img = cv2.imread("uploads/user.jpg")

mp_face_mesh = mp.solutions.face_mesh
mp_draw = mp.solutions.drawing_utils

with mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True
) as face_mesh:

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:

        for face_landmarks in results.multi_face_landmarks:

            mp_draw.draw_landmarks(
                image=img,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION
            )

        cv2.imshow("Landmarks", img)
        cv2.waitKey(0)

cv2.destroyAllWindows()