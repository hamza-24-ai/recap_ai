from typing import List,TypedDict

class AgentPipeline(TypedDict):
    meeting_id: int
    raw_transcript: str
    cleaned_transcript: str
    decisions: List[str]
    action_items: List[dict]