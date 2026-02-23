import joblib
import numpy as np
import torch
from torchvision import transforms
from PIL import Image
from pathlib import Path

from .cnn import load_cnn

MODEL_DIR = Path(__file__).resolve().parent.parent / "models"

# ----------------------------
# Load models once
# ----------------------------
cnn = load_cnn()

xgb_binary = joblib.load(MODEL_DIR / "xgb_binary_metal.pkl")
xgb_stage1 = joblib.load(MODEL_DIR / "xgb_stage1_scrap.pkl")
xgb_metal  = joblib.load(MODEL_DIR / "xgb_model.pkl")

le_stage1 = joblib.load(MODEL_DIR / "label_encoder_stage1.pkl")
le_metal  = joblib.load(MODEL_DIR / "label_encoder.pkl")

# ----------------------------
# Image transform
# ----------------------------
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# ----------------------------
# prediction
# ----------------------------
def predict_local(image: Image.Image):
    device = next(cnn.parameters()).device
    tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        embedding = cnn(tensor).cpu().numpy()

    # Stage 0: Metal detection
    metal_prob = xgb_binary.predict_proba(embedding)[0][1]

    # Non-metal → scrap category
    if metal_prob < 0.6:
        probs = xgb_stage1.predict_proba(embedding)[0]
        idx = np.argmax(probs)
        label = le_stage1.inverse_transform([idx])[0]
        return label, float(probs[idx])

    # Metal → metal type
    probs = xgb_metal.predict_proba(embedding)[0]
    idx = np.argmax(probs)
    label = le_metal.inverse_transform([idx])[0]
    return label, float(probs[idx])
