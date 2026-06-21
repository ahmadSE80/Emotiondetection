import numpy as np
import torch
import torch.nn as nn
import torchvision
from tensorflow.keras.preprocessing import image
from PIL import Image
import torchvision.transforms as T

print("=== FACE SHAPE SCRIPT STARTED ===")

# Load model
model = torchvision.models.efficientnet_b0(weights=None)

model.classifier = nn.Sequential(
    nn.Dropout(0.3),
    nn.Linear(model.classifier[1].in_features, 5)
)

model.load_state_dict(torch.load("models/best_model.pth", map_location="cpu"))

model.eval()

# Class names
classes = ['Heart', 'Oblong', 'Oval', 'Round', 'Square']

# Load image
img = Image.open("uploads/user.jpg").convert("RGB")

transform = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
    T.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

img_tensor = transform(img)
img_tensor = img_tensor.unsqueeze(0)

# Predict
with torch.no_grad():
    outputs = model(img_tensor)
    probabilities = torch.softmax(outputs, dim=1)

prediction = probabilities.numpy()

print("\nAll Probabilities:")
for i, score in enumerate(prediction[0]):
    print(classes[i], ":", round(score * 100, 2), "%")

predicted_class = classes[np.argmax(prediction)]
confidence = np.max(prediction) * 100

print("Predicted Face Shape:", predicted_class)

predicted_class = classes[np.argmax(prediction)]
confidence = np.max(prediction) * 100

face_shape = predicted_class

print("\nFACE SHAPE RESULT")
print("-------------------")
print("Face Shape:", predicted_class)
print("Confidence:", round(confidence, 2), "%")
with open("face_shape_result.txt", "w") as f:
    f.write(predicted_class)

with open("face_shape_result.txt", "w") as f:
    f.write(predicted_class)

print("Saved to face_shape_result.txt")