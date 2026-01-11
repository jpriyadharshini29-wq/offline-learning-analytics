from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float
from datetime import datetime
from app.database import Base

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer)
    concept = Column(String)
    score = Column(Float)
    activity_type = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    synced = Column(Boolean, default=False)

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer)
    present = Column(Boolean)
    date = Column(DateTime, default=datetime.utcnow)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer)
    message = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
