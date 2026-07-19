
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class ActionItem(Base):
    __tablename__ = "action_items"

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False)  # created in
    assignee_name = Column(String, nullable=True)
    task_description = Column(Text, nullable=False)
    deadline = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, default="pending")  # pending / done / overdue
    source_snippet = Column(Text, nullable=True)  # for citation

    last_checked_meeting_id = Column(
        Integer, ForeignKey("meetings.id", ondelete="SET NULL"), nullable=True
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    meeting = relationship("Meeting", back_populates="action_items", foreign_keys=[meeting_id])