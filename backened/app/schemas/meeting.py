from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MeetingCreate(BaseModel):
    project_id: int
    title: str

class MeetingResponse(BaseModel):
    id: int
    project_id: int
    title: str
    file_url: Optional[str] = None
    status: str
    uploaded_at: datetime

    class Config:
        from_attributes = True