import streamlit as st
from agent.graph import graph

st.set_page_config(page_title="AutoStream AI Agent")

# Initialize state
if "state" not in st.session_state:
    st.session_state.state = {
        "messages": [
            {"role": "assistant", "content": "Hi 👋 Ask me about AutoStream pricing, plans, or policies."}
        ],
        "name": None,
        "email": None,
        "platform": None,
    }

st.title("🎬 AutoStream AI Agent")

# Display chat history
for msg in st.session_state.state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message
    st.session_state.state["messages"].append(
        {"role": "user", "content": user_input}
    )

    # Run agent
    st.session_state.state = graph.invoke(st.session_state.state)

    st.rerun()
