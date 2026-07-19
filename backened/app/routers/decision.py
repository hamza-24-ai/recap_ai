from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.decision import Decision
from app.models.meeting import Meeting
from app.models.project import Project
from app.schemas.decision import DecisionResponse
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/decisions", tags=["Decisions"])


@router.get("/meeting/{meeting_id}", response_model=List[DecisionResponse])
def get_decisions_for_meeting(
    meeting_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # ownership check: meeting -> project -> user
    meeting = db.query(Meeting).join(Project).filter(
        Meeting.id == meeting_id, Project.user_id == current_user.id
    ).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    return db.query(Decision).filter(Decision.meeting_id == meeting_id).all()