from fastapi import APIRouter, HTTPException, status
from app.models.user import UserCreate, UserLogin
from app.db.mongo import users_collection
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
def signup(user: UserCreate):
    
    # Prevent duplicate accounts
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(
            status_code=400,
            detail="User already exists",
        )

    # FORCE ROLE = USER (NO ADMIN / DELIVERY)
    users_collection.insert_one({
        "email": user.email,
        "password": hash_password(user.password),
        "role": "user",

        # ACCOUNT FLAGS
        "disabled": False,
        "deleted": False,
        "created_by_admin": False,
        "must_change_password": False,

        # OPTIONAL
        "location": None,
    })

    return {"message": "Signup successful"}

@router.post("/login")
def login(user: UserLogin):
    db_user = users_collection.find_one({"email": user.email})

    # User not found
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Password mismatch
    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Block disabled users
    if db_user.get("disabled"):
        raise HTTPException(
            status_code=403,
            detail="Account disabled. Contact administrator.",
        )

    # Block deleted users
    if db_user.get("deleted"):
        raise HTTPException(
            status_code=403,
            detail="Account deleted. Contact administrator.",
        )

    # Create JWT
    token = create_access_token({
        "sub": db_user["email"],
        "role": db_user["role"],
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": db_user["role"],
        "email": db_user["email"],
        "user_id": str(db_user["_id"]),
        "must_change_password": db_user.get("must_change_password", False),
    }
