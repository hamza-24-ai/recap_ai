
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.core.database import Base

class AgentRunLog(Base):
    __tablename__ = "agent_run_logs"

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False)
    agent_name = Column(String, nullable=False)
    status = Column(String, nullable=False)  # success / failed
    output_json = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())