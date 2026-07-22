from app.agents.state import AgentPipeline
from app.core.database import Session_Local
from app.models.decision import Decision
from app.models.action_item import ActionItem
from app.models.meeting import Meeting
from datetime import datetime

# Implement WebSocket
from app.core.websocket_manager import manager
import asyncio


def save_to_memory(state: AgentPipeline) -> AgentPipeline:

    meeting_id = state["meeting_id"]
    manager.send_status_sync(meeting_id, "saving_data")
    
    db = Session_Local()

    try:
        meeting_id = state["meeting_id"]

        # 1. Decisions save karo
        for decision_text in state.get("decisions", []):
            new_decision = Decision(
                meeting_id=meeting_id,
                decision_text=decision_text,
            )
            db.add(new_decision)

        # 2. Action Items save karo
        for item in state.get("action_items", []):
            deadline_value = None
            if item.get("deadline"):
                try:
                    deadline_value = datetime.strptime(item["deadline"], "%Y-%m-%d")
                except (ValueError, TypeError):
                    deadline_value = None   # agar LLM ne galat format diya, skip karo

            new_action_item = ActionItem(
                meeting_id=meeting_id,
                assignee_name=item.get("assignee_name"),
                task_description=item.get("task_description", ""),
                deadline=deadline_value,
                source_snippet=item.get("source_snippet"),
                status="pending",
            )
            db.add(new_action_item)

        # 3. Meeting ka status "done" update karo
        meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
        if meeting:
            meeting.status = "done"

        db.commit()

    except Exception as e:
        db.rollback()
        print(f"Error saving to memory: {e}")
        # Meeting status ko "failed" bhi kar sakte ho yahan
        raise

    finally:
        db.close()

    return state