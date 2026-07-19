from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    file_url = Column(String, nullable=True)
    file_public_id = Column(String, nullable=True)   # Cloudinary delete ke liye
    short_summary = Column(Text, nullable=True)
    status = Column(String, default="processing")
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Project", back_populates="meetings")
    decisions = relationship("Decision", back_populates="meeting", cascade="all, delete-orphan")
    action_items = relationship(
        "ActionItem",
        back_populates="meeting",
        foreign_keys="ActionItem.meeting_id",
        cascade="all, delete-orphan"
    )