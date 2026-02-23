from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form,
)
from bson import ObjectId
from datetime import datetime
from typing import Dict, Any
import os
import shutil

from app.db.mongo import orders_collection, users_collection
from app.core.security import get_current_user
from app.services.assign_delivery import assign_nearest
from app.services.geocoder import reverse_geocode

router = APIRouter(prefix="/orders", tags=["Orders"])

# ==========================================================
# CONFIG
# ==========================================================
UPLOAD_DIR = "uploads/orders"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ==========================================================
# UTILITIES
# ==========================================================
def validate_object_id(id_str: str) -> ObjectId:
    try:
        return ObjectId(id_str)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")


def serialize_order(order: Dict[str, Any]) -> Dict[str, Any]:
    order["_id"] = str(order["_id"])
    order["user_id"] = str(order["user_id"])

    if order.get("delivery_id"):
        order["delivery_id"] = str(order["delivery_id"])

    return order


# ==========================================================
# PLACE ORDER (USER)
# ==========================================================
@router.post("/place")
def place_order(
    material: str = Form(...),
    weight: float = Form(...),
    estimated_price: float = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    image: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    if current_user["role"] != "user":
        raise HTTPException(status_code=403, detail="Only users can place orders")

    order_id = ObjectId()

    ext = image.filename.split(".")[-1].lower()
    image_name = f"{order_id}.{ext}"
    image_path = os.path.join(UPLOAD_DIR, image_name)

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    address = reverse_geocode(latitude, longitude)

    order_doc = {
        "_id": order_id,
        "user_id": current_user["_id"],
        "user_email": current_user["email"],
        "material": material,
        "weight": weight,
        "estimated_price": estimated_price,
        "image_url": f"/uploads/orders/{image_name}",
        "location": {
            "latitude": latitude,
            "longitude": longitude,
            "address": address,
        },

        # ORDER FLOW
        "status": "pending",  # pending → assigned → collected → completed / rejected
        "rejection_reason": None,

        # DELIVERY FLOW
        "delivery_id": None,
        "delivery_status": None,  # assigned → in_transit → collected → completed
        "delivery_assigned_at": None,
        "delivery_left_at": None,

        # PAYMENT
        "payment_status": "pending",

        # TIMESTAMPS
        "created_at": datetime.utcnow(),
        "approved_at": None,
        "rejected_at": None,
        "collected_at": None,
        "completed_at": None,
    }

    orders_collection.insert_one(order_doc)

    return {
        "message": "Order placed successfully",
        "order_id": str(order_id),
        "status": "pending",
    }


# ==========================================================
# GET MY ORDERS (USER)
# ==========================================================
@router.get("/my")
def get_my_orders(current_user: dict = Depends(get_current_user)):

    if current_user["role"] != "user":
        raise HTTPException(status_code=403, detail="User access only")

    orders = list(
        orders_collection.find(
            {"user_id": current_user["_id"]}
        ).sort("created_at", -1)
    )

    results = []

    for order in orders:

        # Delivery agent details (only if assigned)
        delivery_agent = None
        if order.get("delivery_id"):
            delivery_agent = users_collection.find_one(
                {"_id": order["delivery_id"]},
                {"email": 1, "full_name": 1, "country_code": 1, "phone_number": 1}
            )

        results.append({
            "_id": str(order["_id"]),
            "user_id": str(order["user_id"]),
            "material": order.get("material"),
            "weight": order.get("weight"),
            "estimated_price": order.get("estimated_price"),
            "image_url": order.get("image_url"),
            "location": order.get("location"),

            "status": order.get("status"),
            "delivery_status": order.get("delivery_status"),
            "payment_status": order.get("payment_status"),

            "rejection_reason": order.get("rejection_reason"),  # ✅ FIX

            "created_at": order.get("created_at"),
            "approved_at": order.get("approved_at"),
            "rejected_at": order.get("rejected_at"),
            "collected_at": order.get("collected_at"),
            "completed_at": order.get("completed_at"),

            # Delivery info (only visible when delivery starts)
            "delivery_agent_email": delivery_agent.get("email") if delivery_agent else None,
            "delivery_agent_name": delivery_agent.get("full_name") if delivery_agent else None,
            "delivery_agent_phone": (
                f"{delivery_agent.get('country_code')} {delivery_agent.get('phone_number')}"
                if delivery_agent and delivery_agent.get("phone_number")
                else None
            ),
        })

    return results

# ==========================================================
# GET ALL ORDERS (ADMIN)
# ==========================================================
@router.get("/all")
def get_all_orders(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access only")

    orders = list(
        orders_collection.find().sort("created_at", -1)
    )

    results = []

    for order in orders:

        # Fetch user info
        user = users_collection.find_one(
            {"_id": order["user_id"]},
            {
                "email": 1,
                "payout_details": 1
            }
        )

        results.append({
            "_id": str(order["_id"]),
            "user_id": str(order["user_id"]),
            "delivery_id": str(order["delivery_id"]) if order.get("delivery_id") else None,

            "material": order.get("material"),
            "weight": order.get("weight"),
            "estimated_price": order.get("estimated_price"),
            "image_url": order.get("image_url"),
            "location": order.get("location"),

            "status": order.get("status"),
            "delivery_status": order.get("delivery_status"),
            "payment_status": order.get("payment_status"),
            "rejection_reason": order.get("rejection_reason"),

            "created_at": order.get("created_at"),
            "approved_at": order.get("approved_at"),
            "rejected_at": order.get("rejected_at"),
            "collected_at": order.get("collected_at"),
            "completed_at": order.get("completed_at"),

            # 👇 THIS IS THE FIX
            "user_email": user.get("email") if user else None,
            "payout_details": user.get("payout_details") if user else None,
        })

    return results


# ==========================================================
# APPROVE ORDER (ADMIN)
# ==========================================================
@router.post("/{order_id}/approve")
def approve_order(order_id: str, current_user: dict = Depends(get_current_user)):

    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access only")

    oid = validate_object_id(order_id)
    order = orders_collection.find_one({"_id": oid})

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order["status"] != "pending":
        raise HTTPException(status_code=400, detail="Order already processed")

    delivery_agents = list(
        users_collection.find(
            {
                "role": "delivery",
                "disabled": False,
                "deleted": False,
            }
        )
    )

    if not delivery_agents:
        raise HTTPException(status_code=400, detail="No delivery agents available")

    chosen_agent = assign_nearest(order, delivery_agents)

    orders_collection.update_one(
        {"_id": oid},
        {
            "$set": {
                "status": "assigned",
                "delivery_id": chosen_agent["_id"],
                "delivery_status": "assigned",
                "delivery_assigned_at": datetime.utcnow(),
                "approved_at": datetime.utcnow(),
            }
        },
    )

    return {
        "message": "Order approved and delivery assigned",
        "delivery_agent": chosen_agent["email"],
        "status": "assigned",
    }


# ==========================================================
# REJECT ORDER (ADMIN)
# ==========================================================
@router.post("/{order_id}/reject")
def reject_order(
    order_id: str,
    reason: str = Form(...),
    current_user: dict = Depends(get_current_user),
):

    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access only")

    oid = validate_object_id(order_id)
    order = orders_collection.find_one({"_id": oid})

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order["status"] != "pending":
        raise HTTPException(status_code=400, detail="Order already processed")

    orders_collection.update_one(
        {"_id": oid},
        {
            "$set": {
                "status": "rejected",
                "rejection_reason": reason.strip(),
                "rejected_at": datetime.utcnow(),
            }
        },
    )

    return {"message": "Order rejected", "status": "rejected"}


# ==========================================================
# DELIVERY MARKS JOURNEY STARTED
# ==========================================================
@router.post("/{order_id}/delivery/left")
def delivery_left(order_id: str, current_user: dict = Depends(get_current_user)):

    if current_user["role"] != "delivery":
        raise HTTPException(status_code=403, detail="Delivery only")

    oid = validate_object_id(order_id)
    order = orders_collection.find_one({"_id": oid})

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if str(order.get("delivery_id")) != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not your order")

    orders_collection.update_one(
        {"_id": oid},
        {
            "$set": {
                "delivery_status": "in_transit",
                "delivery_left_at": datetime.utcnow(),
            }
        },
    )

    return {"message": "Delivery started"}


# ==========================================================
# DELIVERY MARKS ORDER COLLECTED
# ==========================================================
@router.post("/{order_id}/delivery/collected")
def delivery_collected(order_id: str, current_user: dict = Depends(get_current_user)):

    if current_user["role"] != "delivery":
        raise HTTPException(status_code=403, detail="Delivery only")

    oid = validate_object_id(order_id)
    order = orders_collection.find_one({"_id": oid})

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if str(order.get("delivery_id")) != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not your order")

    orders_collection.update_one(
        {"_id": oid},
        {
            "$set": {
                "status": "collected",
                "delivery_status": "collected",
                "collected_at": datetime.utcnow(),
            }
        },
    )

    return {"message": "Order collected"}


# ==========================================================
# COMPLETE ORDER (PAYMENT SUCCESS)
# ==========================================================
@router.post("/{order_id}/complete")
def complete_order(order_id: str, current_user: dict = Depends(get_current_user)):

    if current_user["role"] not in ["admin", "delivery"]:
        raise HTTPException(status_code=403, detail="Not allowed")

    oid = validate_object_id(order_id)
    order = orders_collection.find_one({"_id": oid})

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    orders_collection.update_one(
        {"_id": oid},
        {
            "$set": {
                "status": "completed",
                "delivery_status": "completed",
                "payment_status": "paid",
                "completed_at": datetime.utcnow(),
            }
        },
    )

    return {"message": "Order completed successfully"}


# ==========================================================
# ADMIN DELIVERY OVERVIEW
# ==========================================================
@router.get("/admin/delivery/overview")
def delivery_overview(current_user: dict = Depends(get_current_user)):

    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    # Get all delivery agents
    agents = list(users_collection.find({"role": "delivery"}))

    results = []

    for agent in agents:
        agent_id = agent["_id"]

        # ================================
        # Active Orders
        # ================================
        active_orders = orders_collection.count_documents({
            "delivery_id": agent_id,
            "status": {"$in": ["assigned", "collected"]}
        })

        # ================================
        # Completed Orders
        # ================================
        completed_orders = orders_collection.count_documents({
            "delivery_id": agent_id,
            "status": "completed"
        })

        # ================================
        # Rejected / Failed Orders
        # ================================
        rejected_orders = orders_collection.count_documents({
            "delivery_id": agent_id,
            "status": "rejected"
        })

        # ================================
        # Revenue Generated
        # ================================
        revenue_pipeline = [
            {
                "$match": {
                    "delivery_id": agent_id,
                    "status": "completed"
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total": {"$sum": "$estimated_price"}
                }
            }
        ]

        revenue_result = list(orders_collection.aggregate(revenue_pipeline))
        total_revenue = revenue_result[0]["total"] if revenue_result else 0

        # ================================
        # Last Activity (Latest Order Update)
        # ================================
        last_order = orders_collection.find_one(
            {"delivery_id": agent_id},
            sort=[("created_at", -1)]
        )

        last_activity = last_order.get("created_at") if last_order else None

        # ================================
        # Efficiency Calculation
        # ================================
        total_handled = active_orders + completed_orders + rejected_orders

        if total_handled > 0:
            efficiency = round((completed_orders / total_handled) * 100, 2)
        else:
            efficiency = 0

        results.append({
            "_id": str(agent_id),
            "email": agent.get("email"),
            "active_orders": active_orders,
            "completed_orders": completed_orders,
            "rejected_orders": rejected_orders,
            "total_revenue": round(total_revenue, 2),
            "efficiency_percent": efficiency,
            "disabled": agent.get("disabled", False),
            "created_at": agent.get("created_at"),
            "last_activity": last_activity
        })

    return results


# ==========================================================
# USER SUBMITS PAYOUT DETAILS
# ==========================================================
@router.post("/{order_id}/submit-payout-details")
def submit_payout_details(
    order_id: str,
    full_name: str = Form(...),
    country_code: str = Form(...),  # Example: +91
    phone_number: str = Form(...),
    building: str = Form(...),
    flat: str = Form(...),
    area: str = Form(...),
    city: str = Form(...),
    state: str = Form(...),
    pincode: str = Form(...),
    upi_id: str = Form(...),
    current_user: dict = Depends(get_current_user),
):

    # ===============================
    # ROLE CHECK
    # ===============================
    if current_user["role"] != "user":
        raise HTTPException(status_code=403, detail="User only")

    # ===============================
    # VALIDATE ORDER
    # ===============================
    oid = validate_object_id(order_id)
    order = orders_collection.find_one({"_id": oid})

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Ensure user owns this order
    if str(order["user_id"]) != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not your order")

    # ===============================
    # ALLOW ONLY AFTER ADMIN APPROVES
    # ===============================
    if order["status"] != "assigned":
        raise HTTPException(
            status_code=400,
            detail="Payout details can only be submitted after admin approval"
        )

    # ===============================
    # SAVE PAYOUT DETAILS IN USER PROFILE
    # ===============================
    users_collection.update_one(
        {"_id": current_user["_id"]},
        {
            "$set": {
                "payout_details": {
                    "full_name": full_name.strip(),
                    "country_code": country_code.strip(),
                    "phone_number": phone_number.strip(),
                    "building": building.strip(),
                    "flat": flat.strip(),
                    "area": area.strip(),
                    "city": city.strip(),
                    "state": state.strip(),
                    "pincode": pincode.strip(),
                    "upi_id": upi_id.strip(),
                    "updated_at": datetime.utcnow(),
                }
            }
        }
    )

    # ===============================
    # UPDATE ORDER PAYMENT STATUS
    # ===============================
    orders_collection.update_one(
        {"_id": oid},
        {
            "$set": {
                "payment_status": "details_submitted"
            }
        }
    )

    return {
        "message": "Payout details submitted successfully",
        "status": "details_submitted"
    }

# ==========================================================
# DELIVERY PROFILE UPDATE
# ==========================================================
@router.put("/delivery/profile")
def update_delivery_profile(
    full_name: str = Form(...),
    country_code: str = Form(...),
    phone_number: str = Form(...),
    current_user: dict = Depends(get_current_user),
):

    if current_user["role"] != "delivery":
        raise HTTPException(status_code=403, detail="Delivery only")

    users_collection.update_one(
        {"_id": current_user["_id"]},
        {
            "$set": {
                "full_name": full_name.strip(),
                "country_code": country_code.strip(),
                "phone_number": phone_number.strip(),
                "profile_updated_at": datetime.utcnow(),
            }
        }
    )

    return {"message": "Profile updated successfully"}

# ==========================================================
# GET DELIVERY ASSIGNMENTS
# ==========================================================
@router.get("/delivery/my-assignments")
def get_delivery_assignments(current_user: dict = Depends(get_current_user)):

    if current_user["role"] != "delivery":
        raise HTTPException(status_code=403, detail="Delivery only")

    delivery_id = current_user["_id"]

    orders = list(
        orders_collection.find({
            "delivery_id": delivery_id,
            "status": {"$in": ["assigned", "collected"]}
        }).sort("created_at", -1)
    )

    results = []

    for order in orders:
        user = users_collection.find_one({"_id": order["user_id"]})

        results.append({
            "_id": str(order["_id"]),
            "material": order["material"],
            "weight": order["weight"],
            "estimated_price": order["estimated_price"],
            "status": order["status"],
            "delivery_status": order.get("delivery_status"),
            "location": order.get("location"),
            "created_at": order["created_at"],

            "user_email": user.get("email") if user else None,
            "payout_details": user.get("payout_details") if user else None,
        })

    return results
