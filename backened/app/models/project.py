
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="projects")
    meetings = relationship("Meeting", back_populates="project", cascade="all, delete-orphan")