AutoStream – Social-to-Lead Conversational Agent
Project Overview

AutoStream is a fictional SaaS platform that offers automated video editing tools for content creators.
This project implements a conversational AI agent that answers user queries and converts high-intent users into qualified leads using a structured agentic workflow.

The agent is capable of:

Handling greetings and FAQs

Answering pricing and policy queries using a knowledge base

Detecting high-intent users

Collecting lead details in a step-by-step flow

Triggering a mock API only after all required data is collected

 How to Run the Project Locally
1. Clone the Repository
git clone https://github.com/1DS22CS037-ANSHIKAJAISWAL/AutoStream-Agent.git
cd AutoStream-Agent

2. Create and Activate Virtual Environment
python -m venv .venv
.venv\Scripts\activate   # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Run the Application
streamlit run streamlit_app.py


The chatbot interface will open in your browser.

 Architecture Explanation (LangGraph & State Management)

This project uses LangGraph to implement a structured, stateful conversational workflow.
LangGraph was chosen because it allows explicit control over conversation flow, intent handling, and tool execution, which is essential for lead-generation systems.

The agent maintains a shared AgentState that stores:

Conversation history

User name

Email address

Creator platform (YouTube, Instagram, etc.)

Each user message updates the state, allowing the agent to:

Respond with knowledge-based answers for pricing and policies

Detect intent shifts (e.g., from pricing to high-intent)

Ask for missing lead details one step at a time

Prevent premature execution of backend tools

This state-driven design ensures the mock lead capture API is triggered only after all required information is collected, making the workflow reliable and production-ready.

 WhatsApp Deployment Using Webhooks (Conceptual)

To integrate this agent with WhatsApp:

Use WhatsApp Business API (via Meta or Twilio) to receive messages.

Incoming messages are sent to a backend server using webhooks.

The backend forwards messages to the LangGraph agent.

Conversation state is stored in a database (e.g., Redis or PostgreSQL).

Agent responses are sent back to WhatsApp via the API.

When a lead is captured, the backend can:

Store lead data in a CRM

Trigger notifications or follow-ups

This webhook-based approach allows the same agent to be reused across multiple platforms.
