import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# =============================
# ROUTER IMPORTS
# =============================
from app.api.auth import router as auth_router
from app.api.predict import router as predict_router
from app.api.orders import router as orders_router
from app.api.users import router as users_router
from app.api.admin import router as admin_router

# =============================
# CREATE UPLOAD FOLDER
# =============================
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# =============================
# CREATE FASTAPI APP
# =============================
app = FastAPI(
    title="ScrapX API",
    description="AI-powered scrap classification and price estimation",
    version="1.0.0",
)

# =============================
# CORS CONFIG
# =============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================
# STATIC FILES
# =============================
app.mount(
    "/uploads",
    StaticFiles(directory=UPLOAD_DIR),
    name="uploads",
)

# =============================
# INCLUDE ROUTERS
# =============================
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(predict_router)
app.include_router(orders_router)
app.include_router(users_router)

# =============================
# ROOT ENDPOINT
# =============================
@app.get("/")
def root():
    return {"message": "ScrapX backend running successfully"}
