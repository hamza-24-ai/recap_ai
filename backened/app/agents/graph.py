from langgraph.graph import StateGraph, END
from app.agents.state import AgentPipeline
from app.agents.transcript_cleaner import clean_transcript
from app.agents.decision_extractor import extract_decisions
from app.agents.action_item_extractor import extract_action_items
from app.agents.memory_tracker import save_to_memory
from app.agents.follow_up_checker import check_followups


def build_pipeline():
    graph = StateGraph(AgentPipeline)

    # 1. Sab nodes (agents) ko graph mein register karo
    graph.add_node("clean_transcript", clean_transcript)
    graph.add_node("extract_decisions", extract_decisions)
    graph.add_node("extract_action_items", extract_action_items)
    graph.add_node("save_to_memory", save_to_memory)
    graph.add_node("check_followups", check_followups)   # naya node

    # 2. Entry point set karo — sabse pehla node kaunsa chalega
    graph.set_entry_point("clean_transcript")

    # 3. Edges banao — kaunsa node ke baad kaunsa chalega
    graph.add_edge("clean_transcript", "extract_decisions")
    graph.add_edge("extract_decisions", "extract_action_items")
    graph.add_edge("extract_action_items", "save_to_memory")
    graph.add_edge("save_to_memory", "check_followups")   # save ke baad follow-up check
    graph.add_edge("check_followups", END)
    return graph.compile()


# Ek hi baar compile karke rakh lo, baar baar build na karna pade
pipeline = build_pipeline()