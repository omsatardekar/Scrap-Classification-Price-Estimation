import requests
from app.core.config import (
    NYCKEL_CLIENT_ID,
    NYCKEL_CLIENT_SECRET,
    NYCKEL_FUNCTION_ID,
)

TOKEN_URL = "https://www.nyckel.com/connect/token"
INVOKE_URL = f"https://www.nyckel.com/v1/functions/{NYCKEL_FUNCTION_ID}/invoke"

def get_token() -> str | None:
    try:
        response = requests.post(
            TOKEN_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": NYCKEL_CLIENT_ID,
                "client_secret": NYCKEL_CLIENT_SECRET,
            },
            timeout=15,  
        )

        response.raise_for_status()
        return response.json().get("access_token")

    except requests.exceptions.Timeout:
        print("Nyckel token request timed out")
        return None

    except Exception as e:
        print("Nyckel token error:", e)
        return None

def predict_nyckel(image_bytes: bytes):
    """
    Returns:
        (label: str | None, confidence: float | None)
    """

    token = get_token()
    if not token:
        return None, None

    try:
        response = requests.post(
            INVOKE_URL,
            headers={
                "Authorization": f"Bearer {token}",
            },
            files={
                "file": image_bytes
            },
            timeout=25,  
        )

        response.raise_for_status()
        data = response.json()

        label = data.get("labelName")
        confidence = data.get("confidence")

        if label is None or confidence is None:
            print("Nyckel returned invalid response:", data)
            return None, None

        return label, float(confidence)

    except requests.exceptions.Timeout:
        print("Nyckel prediction timed out — fallback will be used")
        return None, None

    except Exception as e:
        print("Nyckel prediction error:", e)
        return None, None
