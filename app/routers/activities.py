from fastapi import APIRouter
from app.database import SessionLocal
from app.models import Activity

router = APIRouter(prefix="/activities")

@router.post("/")
def add_activity(student_id: int, concept: str, score: float, activity_type: str):
    db = SessionLocal()
    activity = Activity(
        student_id=student_id,
        concept=concept,
        score=score,
        activity_type=activity_type
    )
    db.add(activity)
    db.commit()
    return {"message": "Activity recorded"}
