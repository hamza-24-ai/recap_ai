
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Decision(Base):
    __tablename__ = "decisions"

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False)
    decision_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    meeting = relationship("Meeting", back_populates="decisions")