from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ActionItemResponse(BaseModel):
    id: int
    meeting_id: int
    assignee_name: Optional[str] = None
    task_description: str
    deadline: Optional[datetime] = None
    status: str
    source_snippet: Optional[str] = None
    last_checked_meeting_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ActionItemStatusUpdate(BaseModel):
    status: str   # pending / done / overdue

class ActionItemCitationResponse(BaseModel):
    id: int
    task_description: str
    assignee_name: Optional[str] = None
    source_snippet: Optional[str] = None
    meeting_id: int
    meeting_title: str
    meeting_uploaded_at: datetime
    file_url: Optional[str] = None   # taake original file bhi dikha sakein chahen to

    class Config:
        from_attributes = True