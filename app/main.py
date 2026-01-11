from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import students, activities, attendance, alerts

# Create all database tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Offline Learning Analytics System",
    description="Offline-first backend to detect early learning gaps in rural schools",
    version="1.0.0"
)

# Root route (fixes the 'Not Found' issue)
@app.get("/")
def root():
    return {
        "status": "OK",
        "message": "Offline Learning Analytics API is running"
    }

# Include routers
app.include_router(students.router, tags=["Students"])
app.include_router(activities.router, tags=["Activities"])
app.include_router(attendance.router, tags=["Attendance"])
app.include_router(alerts.router, tags=["Alerts"])
