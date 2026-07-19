from pydantic import BaseModel
from datetime import datetime

class DecisionResponse(BaseModel):
    id: int
    meeting_id: int
    decision_text: str
    created_at: datetime

    class Config:
        from_attributes = True