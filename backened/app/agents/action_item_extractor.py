from app.agents.state import AgentPipeline
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import json

# Implement Web Socket
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


def extract_action_items(state: AgentPipeline) -> AgentPipeline:


    meeting_id = state["meeting_id"]
    asyncio.run(manager.send_status(meeting_id, "extracting_action_items"))

    
    cleaned_text = state["cleaned_transcript"]

    prompt = f"""You are a meeting analysis assistant.
        Read the following meeting transcript and identify all ACTION ITEMS (tasks assigned to someone).

        For each action item, extract:
        - assignee_name: who is responsible (if not mentioned, use null)
        - task_description: what needs to be done
        - deadline: when it's due, in "YYYY-MM-DD" format if a specific date is mentioned or can be inferred, otherwise null
        - source_snippet: the exact sentence(s) from the transcript this was extracted from

        Transcript:
        {cleaned_text}

        Return ONLY a valid JSON array like this:
        [
          {{
            "assignee_name": "Ali",
            "task_description": "Send the client report",
            "deadline": "2026-07-25",
            "source_snippet": "Ali, can you send the client report by Friday?"
          }}
        ]

        If no action items were found, return an empty array: []
        Do not include any explanation, only the JSON array.
        """

    response = llm.invoke(prompt)
    raw_output = response.content.strip()

    if raw_output.startswith("```"):
        raw_output = raw_output.strip("`").replace("json", "", 1).strip()

    try:
        action_items = json.loads(raw_output)
    except json.JSONDecodeError:
        action_items = []

    state["action_items"] = action_items
    return state