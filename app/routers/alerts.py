from fastapi import APIRouter
from app.database import SessionLocal
from app.models import Alert, Activity
from app.analytics import find_weak_concepts

router = APIRouter(prefix="/alerts")

@router.post("/generate")
def generate_alerts():
    db = SessionLocal()

    activities = db.query(Activity).all()
    weak_concepts = find_weak_concepts(activities)

    created_alerts = []

    for concept in weak_concepts:
        message = f"Weak concept detected: {concept}"
        alert = Alert(student_id=1, message=message)
        db.add(alert)
        created_alerts.append(message)

    db.commit()

    return {
        "alerts_created": created_alerts
    }

@router.get("/")
def get_alerts():
    db = SessionLocal()
    return db.query(Alert).all()
