from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.action_item import ActionItem
from app.models.meeting import Meeting
from app.models.project import Project
from app.schemas.action_item import ActionItemResponse, ActionItemStatusUpdate
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.action_item import ActionItemCitationResponse

router = APIRouter(prefix="/action-items", tags=["Action Items"])


@router.get("/project/{project_id}", response_model=List[ActionItemResponse])
def get_action_items_for_project(
    project_id: int,
    status: Optional[str] = Query(None),   # filter: pending/done/overdue
    assignee: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = db.query(Project).filter(
        Project.id == project_id, Project.user_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    query = db.query(ActionItem).join(Meeting).filter(Meeting.project_id == project_id)

    if status:
        query = query.filter(ActionItem.status == status)
    if assignee:
        query = query.filter(ActionItem.assignee_name == assignee)

    return query.all()


@router.patch("/{action_item_id}/status", response_model=ActionItemResponse)
def update_action_item_status(
    action_item_id: int,
    update: ActionItemStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    action_item = db.query(ActionItem).join(Meeting).join(Project).filter(
        ActionItem.id == action_item_id, Project.user_id == current_user.id
    ).first()
    if not action_item:
        raise HTTPException(status_code=404, detail="Action item not found")

    action_item.status = update.status
    db.commit()
    db.refresh(action_item)
    return action_item




@router.get("/{action_item_id}/citation", response_model=ActionItemCitationResponse)
def get_action_item_citation(
    action_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    action_item = (
        db.query(ActionItem)
        .join(Meeting)
        .join(Project)
        .filter(
            ActionItem.id == action_item_id,
            Project.user_id == current_user.id,
        )
        .first()
    )

    if not action_item:
        raise HTTPException(status_code=404, detail="Action item not found")

    meeting = action_item.meeting   # relationship se seedha mil jayega

    return ActionItemCitationResponse(
        id=action_item.id,
        task_description=action_item.task_description,
        assignee_name=action_item.assignee_name,
        source_snippet=action_item.source_snippet,
        meeting_id=meeting.id,
        meeting_title=meeting.title,
        meeting_uploaded_at=meeting.uploaded_at,
        file_url=meeting.file_url,
    )