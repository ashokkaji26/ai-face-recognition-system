from fastapi import APIRouter, Query, HTTPException
from datetime import datetime, timezone
from database import users_collection, attendance_collection

router = APIRouter(
    prefix="/admin",
    tags=["Admin Analytics"]
)

# 🔐 Hardcoded admin emails
ADMIN_EMAILS = [
    "kaji@gmail.com",
    "demoadmin@gmail.com"
]


def verify_admin(email: str):
    if email not in ADMIN_EMAILS:
        raise HTTPException(
            status_code=403,
            detail="Admin access only"
        )


# =========================
# 1️⃣ OVERALL STATS
# =========================
@router.get("/stats")
def admin_stats(email: str = Query(...)):
    verify_admin(email)

    total_users = users_collection.count_documents({})
    total_attendance = attendance_collection.count_documents({})

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    today_present = attendance_collection.count_documents({"date": today})

    return {
        "success": True,
        "total_users": total_users,
        "total_attendance_records": total_attendance,
        "present_today": today_present
    }


# =========================
# 2️⃣ USER-WISE ATTENDANCE
# =========================
@router.get("/users-attendance")
def users_attendance(email: str = Query(...)):
    verify_admin(email)

    pipeline = [
        {
            "$group": {
                "_id": "$email",
                "present_days": {"$sum": 1}
            }
        },
        {
            "$sort": {"present_days": -1}
        }
    ]

    attendance_data = list(attendance_collection.aggregate(pipeline))

    users = []
    for record in attendance_data:
        user = users_collection.find_one(
            {"email": record["_id"]},
            {"_id": 0, "name": 1}
        )

        users.append({
            "email": record["_id"],
            "name": user.get("name") if user else "",
            "present_days": record["present_days"]
        })

    return {
        "success": True,
        "total_users": len(users),
        "users": users
    }


# =========================
# 3️⃣ DATE-WISE ATTENDANCE
# =========================
@router.get("/daily-attendance")
def daily_attendance(
    date: str = Query(...),
    email: str = Query(...)
):
    verify_admin(email)

    # ✅ Date format validation (DD-MM-YYYY)
    try:
        datetime.strptime(date, "%d-%m-%Y")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Use DD-MM-YYYY"
        )

    records = attendance_collection.find(
        {"date": date},
        {"_id": 0, "email": 1}
    )

    present_users = [r["email"] for r in records]

    return {
        "success": True,
        "date": date,
        "count": len(present_users),
        "present_users": present_users
    }