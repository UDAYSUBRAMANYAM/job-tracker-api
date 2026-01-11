# app/main.py
from fastapi import FastAPI
from database import Base, engine



from sqlalchemy.orm import relationship
from database import Base

from security import hash_password, verify_password
from auth import create_access_token, decode_access_token

from auth_routes import router as auth_router
from user_routes import router as user_router
from skill_routes import router as skill_router
from job_routes import router as job_router

app = FastAPI(title="Kanban Job Tracker API")

# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(skill_router)
app.include_router(job_router)


@app.get("/")
def root():
    return {"message": "Backend running successfully"}


