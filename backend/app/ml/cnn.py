import torch
import timm
from pathlib import Path

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_DIR = Path(__file__).resolve().parent.parent / "models"


def load_cnn():
    model = timm.create_model(
        "convnext_tiny",
        pretrained=False,
        num_classes=0
    )

    model.load_state_dict(
        torch.load(
            MODEL_DIR / "best_cnn_model.pth",
            map_location=DEVICE
        ),
        strict=False
    )

    model.reset_classifier(0)
    model.to(DEVICE)
    model.eval()

    return model
