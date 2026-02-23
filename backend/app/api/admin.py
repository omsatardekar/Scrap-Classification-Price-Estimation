from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from app.db.mongo import orders_collection, users_collection
from app.core.security import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/stats")
def get_admin_stats(current_user: dict = Depends(get_current_user)):

    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    # =========================
    # ORDER STATS
    # =========================
    pending_orders = orders_collection.count_documents({"status": "pending"})

    approved_orders = orders_collection.count_documents({
        "status": {"$in": ["assigned", "collected", "completed"]}
    })

    active_deliveries = orders_collection.count_documents({
        "status": {"$in": ["assigned", "in_transit", "collected"]}
    })

    completed_orders = orders_collection.count_documents({
        "status": "completed"
    })

    rejected_orders = orders_collection.count_documents({
        "status": "rejected"
    })

    # =========================
    # USER STATS
    # =========================
    total_users = users_collection.count_documents({"role": "user"})
    total_admins = users_collection.count_documents({"role": "admin"})
    total_delivery = users_collection.count_documents({"role": "delivery"})

    disabled_users = users_collection.count_documents({"disabled": True})

    # =========================
    # REVENUE
    # =========================
    pipeline = [
        {"$match": {"status": "completed"}},
        {"$group": {"_id": None, "total": {"$sum": "$estimated_price"}}}
    ]

    revenue_data = list(orders_collection.aggregate(pipeline))
    total_revenue = revenue_data[0]["total"] if revenue_data else 0

    return {
        "pendingOrders": pending_orders,
        "approvedOrders": approved_orders,
        "activeDeliveries": active_deliveries,
        "completedOrders": completed_orders,
        "rejectedOrders": rejected_orders,
        "users": total_users,
        "admins": total_admins,
        "deliveryAgents": total_delivery,
        "disabledUsers": disabled_users,
        "totalRevenue": round(total_revenue, 2),
        "generatedAt": datetime.utcnow(),
    }
