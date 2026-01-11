from fastapi import APIRouter
from app.database import SessionLocal
from app.models import Student

router = APIRouter(prefix="/students")

@router.post("/")
def add_student(name: str):
    db = SessionLocal()
    student = Student(name=name)
    db.add(student)
    db.commit()
    return {"message": "Student added"}
