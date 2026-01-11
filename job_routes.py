# app/job_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from deps import get_db
from models import Job, User
from schemas import JobCreate, JobUpdate, JobOut
from auth import get_current_user

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


db = Depends(get_db)


# ---- CREATE JOB ----
@router.post("/", response_model=JobOut, status_code=status.HTTP_201_CREATED)
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_job = Job(
        company_name=job.company_name,
        role=job.role,
        status=job.status,
        apply_link=job.apply_link,
        description=job.description,
        user_id=current_user.id
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job


# ---- GET ALL JOBS (KANBAN LOAD) ----
@router.get("/", response_model=list[JobOut])
def get_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    jobs = db.query(Job).filter(
        Job.user_id == current_user.id
    ).all()

    return jobs


# ---- UPDATE JOB (DRAG & DROP) ----
@router.put("/{job_id}", response_model=JobOut)
def update_job_status(
    job_id: int,
    job: JobUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_job = db.query(Job).filter(
        Job.id == job_id,
        Job.user_id == current_user.id
    ).first()

    if not existing_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    existing_job.status = job.status
    db.commit()
    db.refresh(existing_job)

    return existing_job


# ---- DELETE JOB ----
@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.user_id == current_user.id
    ).first()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    db.delete(job)
    db.commit()
    return
