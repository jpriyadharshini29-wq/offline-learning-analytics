from fastapi import APIRouter
from app.database import SessionLocal
from app.models import Attendance

router = APIRouter(prefix="/attendance")

@router.post("/")
def mark_attendance(student_id: int, present: bool):
    db = SessionLocal()
    record = Attendance(student_id=student_id, present=present)
    db.add(record)
    db.commit()
    return {"message": "Attendance marked"}
