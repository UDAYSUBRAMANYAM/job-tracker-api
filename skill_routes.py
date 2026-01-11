# app/skill_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from deps import get_db
from auth import get_current_user
from models import Skill, User
from schemas import SkillCreate, SkillOut

router = APIRouter(
    prefix="/skills",
    tags=["Skills"]
)


db = Depends(get_db)



# ---- ADD SKILL ----
@router.post("/", response_model=SkillOut, status_code=status.HTTP_201_CREATED)
def add_skill(
    skill: SkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_skill = Skill(
        name=skill.name,
        user_id=current_user.id
    )

    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)

    return new_skill


# ---- GET ALL SKILLS ----
@router.get("/", response_model=list[SkillOut])
def get_skills(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    skills = db.query(Skill).filter(
        Skill.user_id == current_user.id
    ).all()

    return skills


# ---- DELETE SKILL ----
@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    skill = db.query(Skill).filter(
        Skill.id == skill_id,
        Skill.user_id == current_user.id
    ).first()

    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )

    db.delete(skill)
    db.commit()

    return
