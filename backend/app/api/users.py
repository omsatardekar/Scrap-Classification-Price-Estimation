from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId
from datetime import datetime

from app.core.security import (
    get_current_user,
    hash_password,
    verify_password,
)
from app.db.mongo import users_collection, orders_collection
from app.utils.geocode import reverse_geocode

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/location")
def save_location(
    data: dict,
    current_user: dict = Depends(get_current_user),
):
    if current_user["role"] == "admin":
        return {"message": "Admin location not required"}

    lat = data.get("latitude")
    lon = data.get("longitude")

    if lat is None or lon is None:
        raise HTTPException(status_code=400, detail="Latitude & longitude required")

    address = reverse_geocode(lat, lon)

    users_collection.update_one(
        {"_id": current_user["_id"]},
        {
            "$set": {
                "location": {
                    "latitude": lat,
                    "longitude": lon,
                    "address": address,
                }
            }
        }
    )

    return {"message": "Location saved successfully"}

class ProfileUpdate(BaseModel):
    email: EmailStr
    current_password: str
    new_password: Optional[str] = None


@router.put("/profile")
def update_profile(
    payload: ProfileUpdate,
    current_user: dict = Depends(get_current_user),
):
    if not verify_password(payload.current_password, current_user["password"]):
        raise HTTPException(status_code=401, detail="Current password is incorrect")

    update_data = {"email": payload.email}

    if payload.new_password:
        update_data["password"] = hash_password(payload.new_password)

    users_collection.update_one(
        {"_id": current_user["_id"]},
        {"$set": update_data},
    )

    return {"message": "Profile updated successfully"}

@router.get("/all")
def get_all_users(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access only")

    users = []
    for user in users_collection.find({}, {"password": 0}):
        user["_id"] = str(user["_id"])
        user["disabled"] = user.get("disabled", False)
        user["deleted"] = user.get("deleted", False)
        users.append(user)

    return users

class CreateStaffUser(BaseModel):
    email: EmailStr
    password: str
    role: str  # admin | delivery


@router.post("/create")
def create_admin_or_delivery(
    payload: CreateStaffUser,
    current_user: dict = Depends(get_current_user),
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access only")

    if payload.role not in ["admin", "delivery"]:
        raise HTTPException(
            status_code=400,
            detail="Only admin or delivery accounts allowed",
        )

    if users_collection.find_one({"email": payload.email}):
        raise HTTPException(status_code=400, detail="Email already exists")

    users_collection.insert_one(
        {
            "email": payload.email,
            "password": hash_password(payload.password),
            "role": payload.role,
            "disabled": False,
            "deleted": False,
            "created_by_admin": True,
            "must_change_password": True,
            "created_at": datetime.utcnow(),
        }
    )

    return {
        "message": f"{payload.role.capitalize()} account created successfully",
        "email": payload.email,
        "role": payload.role,
    }

@router.get("/{user_id}/active-orders")
def get_user_active_orders(
    user_id: str,
    current_user: dict = Depends(get_current_user),
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access only")

    user_info = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user_info:
        raise HTTPException(status_code=404, detail="User not found")

    role = user_info.get("role")
    active_orders = []

    if role == "user":
        active_orders = list(orders_collection.find(
            {
                "user_id": ObjectId(user_id),
                "status": {"$in": ["pending", "assigned", "collected"]}
            },
            {"_id": 1, "status": 1, "created_at": 1, "material": 1}
        ))
    elif role == "delivery":
        active_orders = list(orders_collection.find(
            {
                "delivery_id": ObjectId(user_id),
                "status": {"$in": ["assigned", "collected"]}
            },
            {"_id": 1, "status": 1, "created_at": 1, "material": 1}
        ))

    # Convert ObjectIds to strings
    for order in active_orders:
        order["_id"] = str(order["_id"])

    return {"active_orders": active_orders, "count": len(active_orders)}

@router.put("/{user_id}/disable")
def disable_user(
    user_id: str,
    current_user: dict = Depends(get_current_user),
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access only")

    user_to_disable = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user_to_disable:
        raise HTTPException(status_code=404, detail="User not found")

    role = user_to_disable.get("role")
    active_orders_count = 0
    if role == "user":
        active_orders_count = orders_collection.count_documents({
            "user_id": ObjectId(user_id),
            "status": {"$in": ["pending", "assigned", "collected"]}
        })
    elif role == "delivery":
        active_orders_count = orders_collection.count_documents({
            "delivery_id": ObjectId(user_id),
            "status": {"$in": ["assigned", "collected"]}
        })

    if active_orders_count > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot disable {role} with active orders"
        )

    users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"disabled": True}},
    )

    return {"message": "User disabled successfully"}

@router.delete("/{user_id}")
def delete_user(
    user_id: str,
    current_user: dict = Depends(get_current_user),
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    # Check if there are any historical orders involving this user
    has_orders = orders_collection.count_documents({
        "$or": [
            {"user_id": ObjectId(user_id)},
            {"delivery_id": ObjectId(user_id)}
        ]
    }) > 0

    if has_orders:
        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "deleted": True,
                    "disabled": True,
                    "deleted_at": datetime.utcnow(),
                }
            },
        )
    else:
        users_collection.delete_one({"_id": ObjectId(user_id)})

    return {"message": "User deleted safely"}


class PayoutDetailsRequest(BaseModel):
    building: str = Field(..., min_length=3, max_length=120)
    flat: str = Field(..., min_length=1, max_length=20)
    area: str = Field(..., min_length=2, max_length=120)
    city: str = Field(..., min_length=2, max_length=100)
    state: str = Field(..., min_length=2, max_length=100)
    pincode: str = Field(..., pattern="^[0-9]{6}$")
    upi_id: str = Field(..., min_length=5, max_length=100)


@router.put("/payout-details")
def update_payout_details(
    payload: PayoutDetailsRequest,
    current_user: dict = Depends(get_current_user),
):
    if current_user["role"] != "user":
        raise HTTPException(status_code=403, detail="User only")

    if "@" not in payload.upi_id:
        raise HTTPException(status_code=400, detail="Invalid UPI ID format")

    result = users_collection.update_one(
        {"_id": ObjectId(current_user["_id"])},
        {
            "$set": {
                "payout_details": payload.model_dump(),
                "payout_updated_at": datetime.utcnow(),
            }
        },
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Payout details saved successfully"}


@router.get("/me")
def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    user = users_collection.find_one(
        {"_id": ObjectId(current_user["_id"])},
        {"password": 0}
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user["_id"] = str(user["_id"])
    return user
