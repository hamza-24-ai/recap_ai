from app.agents.state import AgentPipeline
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

# LLM GROQ SETUP 

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL
)

def clean_transcript(state : AgentPipeline) -> AgentPipeline:

    raw = state["raw_transcript"]

    prompt = f"""You are a transcript cleaning assistant.
        Clean up the following meeting transcript: fix broken formatting, 
        remove filler words (um, uh), and clearly label speakers if identifiable.
        Do not summarize or remove any actual content/information.

        Transcript:
        {raw}

        Return only the cleaned transcript text, nothing else.
        """
    
    response = llm.invoke(prompt)
    cleaned_transcript = response.content

    state["cleaned_transcript"] = cleaned_transcript

    return state