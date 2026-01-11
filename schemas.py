# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import List,Optional
from enum import Enum

class JobStatus(str, Enum):
    saved = "saved"
    applied = "applied"
    interviewed = "interviewed"
    accepted = "accepted"
# -------- USER --------
class UserCreate(BaseModel):
    email: EmailStr
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


# -------- SKILL --------
class SkillCreate(BaseModel):
    name: str


class SkillOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


# -------- JOB --------
class JobCreate(BaseModel):
    company_name: str
    role: str
    status: JobStatus
    apply_link: Optional[str] = None
    description: Optional[str] = None

class JobUpdate(BaseModel):
    status: JobStatus

class JobOut(BaseModel):
    id: int
    company_name: str
    role: str
    status: str

    class Config:
        orm_mode = True
