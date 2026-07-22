from app.agents.state import AgentPipeline
from app.core.database import Session_Local
from app.models.action_item import ActionItem
from app.models.meeting import Meeting
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from datetime import datetime
import json

# Implement WebSocklet

from app.core.websocket_manager import manager
import asyncio

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

# LLM GROQ SETUP 

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL
)


def check_followups(state: AgentPipeline) -> AgentPipeline:

    meeting_id = state["meeting_id"]
    manager.send_status_sync(meeting_id, "checking_followups")

    db = Session_Local()

    try:
        meeting_id = state["meeting_id"]
        cleaned_text = state["cleaned_transcript"]

        # 1. Current meeting ka project nikalo
        current_meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
        if not current_meeting:
            return state

        project_id = current_meeting.project_id

        # 2. Isi project ke sare "pending" action items nikalo
        #    (current meeting ko chhod kar — kyunke wo abhi khud create hui hai)
        # pending_items = (
        #     db.query(ActionItem)
        #     .join(Meeting)
        #     .filter(
        #         Meeting.project_id == project_id,
        #         ActionItem.status == "pending",
        #         ActionItem.meeting_id != meeting_id,
        #     )
        #     .all()
        # )

        pending_items = (
            db.query(ActionItem)
            .join(Meeting, ActionItem.meeting_id == Meeting.id)   # explicit join condition
            .filter(
                Meeting.project_id == project_id,
                ActionItem.status == "pending",
                ActionItem.meeting_id != meeting_id,
            )
            .all()
        )

        # 3. Agar koi pending item nahi hai, to kuch check karne ki zaroorat nahi
        if not pending_items:
            db.close()
            return state

        # 4. Pending items ko LLM-friendly format mein convert karo
        pending_list_for_prompt = [
            {
                "id": item.id,
                "assignee_name": item.assignee_name,
                "task_description": item.task_description,
                "deadline": item.deadline.strftime("%Y-%m-%d") if item.deadline else None,
            }
            for item in pending_items
        ]

        today = datetime.utcnow().strftime("%Y-%m-%d")

        prompt = f"""You are tracking task follow-ups across meetings.
        Today's date is {today}.

        Here is a list of previously PENDING action items:
        {json.dumps(pending_list_for_prompt, indent=2)}

        Here is a NEW meeting transcript:
        {cleaned_text}

        For each pending item, decide its new status:
        - "done" if the transcript mentions it was completed
        - "overdue" if the deadline has passed and there's no mention of completion
        - "pending" if there's no relevant update and the deadline hasn't passed

        Return ONLY a valid JSON array like this:
        [
          {{"id": 5, "status": "done"}},
          {{"id": 7, "status": "overdue"}}
        ]

        Only include items whose status should CHANGE. If nothing changes, return an empty array: []
        """

        response = llm.invoke(prompt)
        raw_output = response.content.strip()

        if raw_output.startswith("```"):
            raw_output = raw_output.strip("`").replace("json", "", 1).strip()

        try:
            updates = json.loads(raw_output)
        except json.JSONDecodeError:
            updates = []

        # 5. DB mein status updates apply karo
        for update in updates:
            item = db.query(ActionItem).filter(ActionItem.id == update["id"]).first()
            if item:
                item.status = update["status"]
                item.last_checked_meeting_id = meeting_id

        db.commit()

    except Exception as e:
        db.rollback()
        print(f"Error in follow-up checker: {e}")

    finally:
        db.close()

    manager.send_status_sync(meeting_id, "done")

    return state