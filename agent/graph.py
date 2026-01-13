from typing import TypedDict, List, Dict, Optional
from langgraph.graph import StateGraph
from agent.rag import retrieve_knowledge
from agent.tools import mock_lead_capture


try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-1.5-flash-latest",
        temperature=0
    )
except:
    llm = None


class AgentState(TypedDict):
    messages: List[Dict[str, str]]  # {"role": "user"/"assistant", "content": str}
    name: Optional[str]
    email: Optional[str]
    platform: Optional[str]

# Intent Detection (FIXED PRIORITY)

def detect_intent(user_msg: str) -> str:
    msg = user_msg.lower()

    #  HIGH INTENT MUST COME FIRST
    if any(x in msg for x in ["i want to", "try", "sign up", "get started", "subscribe"]):
        return "high_intent"

    if "policy" in msg or "refund" in msg or "support" in msg:
        return "policy"

    if "price" in msg or "pricing" in msg or "plan" in msg:
        return "pricing"

    if msg in ["hi", "hello", "hey"]:
        return "greeting"

    return "other"



# Agent Node

def agent_node(state: AgentState):
    user_msg = state["messages"][-1]["content"]
    intent = detect_intent(user_msg)


    # Capture user replies FIRST

    if len(state["messages"]) >= 2:
        last_assistant_msg = state["messages"][-2]["content"].lower()

        if "may i know your name" in last_assistant_msg:
            state["name"] = user_msg

        elif "email" in last_assistant_msg:
            state["email"] = user_msg

        elif "which platform" in last_assistant_msg:
            state["platform"] = user_msg

    # ------------------
    # Greeting
    # ------------------
    if intent == "greeting" and len(state["messages"]) == 1:
        return {
            **state,
            "messages": state["messages"] + [{
                "role": "assistant",
                "content": "Hi 👋 I can help you with AutoStream pricing, plans, or getting started."
            }]
        }

    # ------------------
    # Pricing / Policy (RAG)
    # ------------------
    if intent in ["pricing", "policy"]:
        return {
            **state,
            "messages": state["messages"] + [{
                "role": "assistant",
                "content": retrieve_knowledge(user_msg)
            }]
        }

    # ------------------
    # High Intent - Lead Flow
    # ------------------
    if intent == "high_intent" or any([state["name"], state["email"], state["platform"]]):

        if state["name"] is None:
            return {
                **state,
                "messages": state["messages"] + [{
                    "role": "assistant",
                    "content": "Great! May I know your name?"
                }]
            }

        if state["email"] is None:
            return {
                **state,
                "messages": state["messages"] + [{
                    "role": "assistant",
                    "content": "Thanks! Please share your email address."
                }]
            }

        if state["platform"] is None:
            return {
                **state,
                "messages": state["messages"] + [{
                    "role": "assistant",
                    "content": "Which platform do you create content on? (YouTube, Instagram, etc.)"
                }]
            }

        #  Tool execution ONLY now
        mock_lead_capture(
            state["name"],
            state["email"],
            state["platform"]
        )

        return {
            **state,
            "messages": state["messages"] + [{
                "role": "assistant",
                "content": "✅ Lead captured successfully! Our team will contact you shortly."
            }]
        }

    # ------------------
    # Fallback
    # ------------------
    return {
        **state,
        "messages": state["messages"] + [{
            "role": "assistant",
            "content": "I can help with pricing, plans, or signing up."
        }]
    }



# -------------------------
# Graph Construction
# -------------------------
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.set_entry_point("agent")
graph = graph.compile()


