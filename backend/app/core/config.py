import os
from dotenv import load_dotenv

load_dotenv()

# -------------------------------
# SECURITY / JWT
# -------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "scrapx_super_secret_key_123")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 12


# -------------------------------
# DATABASE
# -------------------------------
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017"
)
DB_NAME = "scrapx"

NYCKEL_CLIENT_ID = os.getenv("NYCKEL_CLIENT_ID", "")
NYCKEL_CLIENT_SECRET = os.getenv("NYCKEL_CLIENT_SECRET", "")
NYCKEL_FUNCTION_ID = os.getenv("NYCKEL_FUNCTION_ID", "")

LOCAL_CONF_THRESHOLD = float(os.getenv("LOCAL_CONF_THRESHOLD", 0.75))
