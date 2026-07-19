from app.agents.state import AgentPipeline
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import json

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

# LLM GROQ SETUP 

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL
)

def extract_decisions(state : AgentPipeline) -> AgentPipeline:
    raw_text = state["cleaned_transcript"]

    prompt = f"""You are a meeting analysis assistant.
        Read the following meeting transcript and identify all key DECISIONS that were made.
        A decision is something the team agreed on or finalized not a task assignment, just the decision itself.

        Transcript:
        {raw_text}

        Return ONLY a valid JSON array of strings, like this:
        ["Decision 1 text", "Decision 2 text"]

        If no decisions were made, return an empty array: []
        Do not include any explanation, only the JSON array.
        """
    
    response = llm.invoke(prompt)
    decisions_text = response.content.strip()

    # Sometimes LLMs wrap JSON in ```json ... ``` — clean that up
    if decisions_text.startswith("```"):
        decisions_text = decisions_text.strip("`").replace("json", "", 1).strip()

    try:
        decisions = json.loads(decisions_text)
    except json.JSONDecodeError:
        decisions = []   # agar LLM ne galat format diya, empty list se aage badho (crash mat karo)

    state["decisions"] = decisions
    return state
