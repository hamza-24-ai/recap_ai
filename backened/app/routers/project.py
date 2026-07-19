from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectResponse
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_project = Project(name=project.name, user_id=current_user.id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


@router.get("/", response_model=List[ProjectResponse])
def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Project).filter(Project.user_id == current_user.id).all()


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = db.query(Project).filter(
        Project.id == project_id, Project.user_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = db.query(Project).filter(
        Project.id == project_id, Project.user_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # NOTE: agar project ke andar meetings hain jinki files Cloudinary pe hain,
    # unhe bhi loop karke delete karna chahiye pehle (cascading delete rule)
    from app.models.meeting import Meeting
    from app.core.cloudinary import delete_transcript

    meetings = db.query(Meeting).filter(Meeting.project_id == project_id).all()
    for meeting in meetings:
        if meeting.file_public_id:
            delete_transcript(meeting.file_public_id)

    db.delete(project)   # cascade se meetings/decisions/action_items khud delete ho jayenge DB se
    db.commit()

    return {"message": "Project deleted successfully"}