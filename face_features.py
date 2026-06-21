import cv2
import mediapipe as mp
import math
import numpy as np
import os


with open("face_shape_result.txt", "r") as f:
    predicted_class = f.read().strip()

print("Face Shape:", predicted_class)

mp_face_mesh = mp.solutions.face_mesh

image_path = "uploads/user.jpg"

frame = cv2.imread(image_path)

if frame is None:
    print("Image not found!")
    exit()

with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True) as face_mesh:

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if not results.multi_face_landmarks:
        print("No face detected!")
        exit()

    face = results.multi_face_landmarks[0]

    h, w, _ = frame.shape

    def point(index):
        lm = face.landmark[index]
        return int(lm.x * w), int(lm.y * h)
    upper_lip_points = [
    61,185,40,39,37,0,267,269,270,409,291
]

    lower_lip_points = [
    61,146,91,181,84,17,314,405,321,375,291
]
    

    # =====================================
    # EYE ANALYSIS
    # =====================================

    inner = point(133)
    outer = point(33)

    top = point(159)
    bottom = point(145)

    eyebrow = point(70)

    eye_width = math.dist(inner, outer)
    eye_height = math.dist(top, bottom)

    ratio = eye_width / eye_height

    if ratio > 2.5:
        eye_type = "Almond"
    else:
        eye_type = "Round"

    brow_lid_distance = abs(eyebrow[1] - top[1])

    hood_ratio = brow_lid_distance / eye_height

    if hood_ratio < 1.5:
        hooded = "Yes"
    else:
        hooded = "No"

    slope = outer[1] - inner[1]

    if slope < -5:
        orientation = "Upturned"
    elif slope > 5:
        orientation = "Downturned"
    else:
        orientation = "Neutral"

    left_center = (
        (inner[0] + outer[0]) // 2,
        (inner[1] + outer[1]) // 2
    )

    r_inner = point(362)
    r_outer = point(263)

    right_center = (
        (r_inner[0] + r_outer[0]) // 2,
        (r_inner[1] + r_outer[1]) // 2
    )

    eye_gap = math.dist(left_center, right_center)

    if eye_gap < eye_width * 2:
        spacing = "Close Set"
    else:
        spacing = "Wide Set"

    # =====================================
    # LIP ANALYSIS
    # =====================================

    left_lip = point(61)
    right_lip = point(291)

    upper_lip_top = point(0)
    upper_lip_bottom = point(13)

    lower_lip_top = point(14)
    lower_lip_bottom = point(17)

    lip_width = math.dist(left_lip, right_lip)

    upper_lip_height = math.dist(
        upper_lip_top,
        upper_lip_bottom
    )

    lower_lip_height = math.dist(
        lower_lip_top,
        lower_lip_bottom
    )

    total_lip_height = (
        upper_lip_height +
        lower_lip_height
    )
    print("Upper Lip Height:", upper_lip_height)
    print("Lower Lip Height:", lower_lip_height)
    print("Total Lip Height:", total_lip_height)
    print("Lip Width:", lip_width)

    lip_ratio = lower_lip_height / upper_lip_height

    if total_lip_height < 60:
        lip_type = "Thin Lips"

    elif total_lip_height > 95:
        lip_type = "Full Lips"

    elif lip_ratio > 2.2:
        lip_type = "Heavy Lower"

    elif lip_ratio < 0.6:
        lip_type = "Heavy Upper"

    else:
        lip_type = "Balanced Lips"

    # =====================================
    # NOSE ANALYSIS
    # =====================================

    nose_left = point(90)
    nose_right = point(320)

    nose_width = math.dist(
        nose_left,
        nose_right
    )

    face_left = point(234)
    face_right = point(454)

    face_width = math.dist(face_left, face_right)

    nose_ratio = nose_width / face_width

    print("Nose Ratio:", nose_ratio)
    print("Nose Width:", nose_width)
    print("Face Width:", face_width)
    print("Nose Ratio:", nose_ratio)

    if nose_ratio < 0.27:
        nose_type = "Narrow Nose"

    elif nose_ratio < 0.36:
        nose_type = "Medium Nose"

    else:
        nose_type = "Wide Nose"

    # =====================================
    # PRINT RESULTS
    # =====================================

    print("\nFACE FEATURE ANALYSIS")
    print("========================")

    print("\nEYES")
    print("------------------------")
    print("Eye Type   :", eye_type)
    print("Eye Angle  :", orientation)
    print("Spacing    :", spacing)
    print("Hooded     :", hooded)

    print("\nLIPS")
    print("------------------------")
    print("Lip Type   :", lip_type)
    
    # =====================================
    # LIPSTICK SIMULATION
    # =====================================

    upper = []
    for idx in upper_lip_points:
        upper.append(point(idx))

    upper = np.array(upper, dtype=np.int32)

    lower = []
    for idx in lower_lip_points:
        lower.append(point(idx))

    lower = np.array(lower, dtype=np.int32)

    overlay = frame.copy()

# Choose lipstick color based on lip type
if lip_type == "Full Lips":
    lipstick_color = (120, 50, 200)      # Nude

elif lip_type == "Heavy Upper":
    lipstick_color = (40, 0, 120)      # Mauve

elif lip_type == "Heavy Lower":
    lipstick_color = (0, 0, 255)         # Red

elif lip_type == "Thin Lips":
    lipstick_color = (180, 105, 255)     # Pink

else:
    lipstick_color = (80, 80, 200)       # Rose

# Apply lipstick
cv2.fillPoly(overlay, [upper], lipstick_color)
cv2.fillPoly(overlay, [lower], lipstick_color)

frame = cv2.addWeighted(
    overlay,
    0.35,
    frame,
    0.65,
    0
)

print("\nNOSE")
print("------------------------")
print("Nose Type  :", nose_type)

  # =====================================
# GLASSES SIMULATION
# =====================================

# Select glasses based on face shape

if predicted_class == "Round":
    glass_path = "assets/glasses/rectangle_glass.png"

elif predicted_class == "Square":
    glass_path = "assets/glasses/round_glass.png"

elif predicted_class == "Oval":
    glass_path = "assets/glasses/cat_eye_glass.png"

elif predicted_class == "Heart":
    glass_path = "assets/glasses/rimless_glass.png"

else:  # Oblong
    glass_path = "assets/glasses/aviatar_glass.png"

glass_img = cv2.imread(
    glass_path,
    cv2.IMREAD_UNCHANGED
)

if glass_img is not None:

    left_eye = point(33)
    right_eye = point(263)

    eye_distance = int(
        math.dist(left_eye, right_eye)
    )

    glass_width = int(eye_distance * 1.8)

    scale = glass_width / glass_img.shape[1]

    glass_height = int(
        glass_img.shape[0] * scale
    )

    glass_img = cv2.resize(
        glass_img,
        (glass_width, glass_height)
    )

    center_x = (left_eye[0] + right_eye[0]) // 2
    center_y = (left_eye[1] + right_eye[1]) // 2

    x = center_x - glass_width // 2
    y = center_y - glass_height // 2

    if x < 0:
        x = 0

    if y < 0:
        y = 0

    if x + glass_width > w:
        glass_width = w - x

    if y + glass_height > h:
        glass_height = h - y

    glass_img = glass_img[
        0:glass_height,
        0:glass_width
    ]

    alpha = glass_img[:, :, 3] / 255.0

    for c in range(3):

        frame[
            y:y+glass_height,
            x:x+glass_width,
            c
        ] = (
            alpha * glass_img[:, :, c]
            +
            (1 - alpha) *
            frame[
                y:y+glass_height,
                x:x+glass_width,
                c
            ]
        )
    print("Glass Path:", glass_path)
    print("Glass Loaded:", glass_img is not None)
  
# =====================================
# FACIAL SYMMETRY
# =====================================

face_center_x = point(1)[0]

left_eye_x = point(33)[0]
right_eye_x = point(263)[0]

left_mouth_x = point(61)[0]
right_mouth_x = point(291)[0]

eye_diff = abs(
    (face_center_x - left_eye_x)
    -
    (right_eye_x - face_center_x)
)

mouth_diff = abs(
    (face_center_x - left_mouth_x)
    -
    (right_mouth_x - face_center_x)
)

symmetry_error = (eye_diff + mouth_diff) / 2

facial_symmetry = max(
    0,
    100 - symmetry_error
)

facial_symmetry = round(facial_symmetry, 1)
# =====================================
# BEAUTY SCORE
# =====================================

beauty_score = 50

# symmetry weight
beauty_score += facial_symmetry * 0.3

# face shape
if predicted_class == "Oval":
    beauty_score += 10

elif predicted_class == "Heart":
    beauty_score += 8

elif predicted_class == "Square":
    beauty_score += 7

elif predicted_class == "Round":
    beauty_score += 6

elif predicted_class == "Oblong":
    beauty_score += 6

# eye shape
if eye_type == "Almond":
    beauty_score += 8

elif eye_type == "Round":
    beauty_score += 5

# lips
if lip_type == "Full Lips":
    beauty_score += 7

elif lip_type == "Heavy Lower":
    beauty_score += 5

# nose
if nose_type == "Narrow Nose":
    beauty_score += 7

elif nose_type == "Medium Nose":
    beauty_score += 5

beauty_score = min(100, round(beauty_score))

print("Beauty Score:", beauty_score)
print("Facial Symmetry:", facial_symmetry)

cv2.imshow("Face Feature Analysis", frame)

with open("face_features_result.txt", "w") as f:
    f.write(f"{eye_type}\n")
    f.write(f"{lip_type}\n")
    f.write(f"{nose_type}\n")
    
facial_symmetry = round(facial_symmetry)

beauty_score = round(
    facial_symmetry * 0.7 +
    30
)

print("Beauty Score:", beauty_score)
print("Facial Symmetry:", facial_symmetry)

with open("symmetry_result.txt", "w") as f:
    f.write(str(facial_symmetry))

with open("beauty_score.txt", "w") as f:
    f.write(str(beauty_score))

os.makedirs("results", exist_ok=True)

saved = cv2.imwrite(
    "results/final_simulation.jpg",
    frame
)

print("Image Saved:", saved)

cv2.imshow("Face Feature Analysis", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Files saved successfully")

cv2.waitKey(0)
cv2.destroyAllWindows()

print("Saved face_features_result.txt")