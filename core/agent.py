# agent.py
import asyncio
from core.constants import composio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI

import os
from dotenv import load_dotenv

load_dotenv()


class GoogleWorkspaceCopilot:
    """
    AI Agent for Google Workspace using Composio Tool Router and LangChain MCP client.
    Toolkits: Gmail, Docs, Sheets, Presentation
    """

    def __init__(self):
        self.sessions = {}  # user_id -> session info
        self.clients = {}   # user_id -> MultiServerMCPClient
        self.composio = composio
        self.conversation_history = {}

    async def create_session_for_user(self, user_email: str) -> str:
        """Create a Tool Router session for a user if it doesn't exist."""
        if user_email in self.sessions:
            return self.sessions[user_email]['url']

        session = self.composio.experimental.tool_router.create_session(
            user_id=user_email,
            toolkits=[
                {'toolkit': 'gmail', 'auth_config_id': os.getenv("GMAIL_AUTH_CONFIG_ID")},
                {'toolkit': 'googledocs', 'auth_config_id': os.getenv("DOCS_AUTH_CONFIG_ID")},
                {'toolkit': 'googlesheets', 'auth_config_id': os.getenv("SHEETS_AUTH_CONFIG_ID")},
                {'toolkit': 'googleslides', 'auth_config_id': os.getenv("SLIDES_AUTH_CONFIG_ID")},

            ],
        )
        self.sessions[user_email] = session
        return session['url']

    async def setup_mcp_client(self, user_email: str) -> MultiServerMCPClient:
        """Set up LangChain MCP client for a user."""
        if user_email in self.clients:
            return self.clients[user_email]

        mcp_url = await self.create_session_for_user(user_email)
        client = MultiServerMCPClient(
            {
                "composio": {
                    "url": mcp_url,
                    "transport": "streamable_http"  # recommended transport
                }
            }
        )
        self.clients[user_email] = client
        return client

    async def run_command(self, user_email: str, prompt: str):
        client = await self.setup_mcp_client(user_email)
        model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            api_key=os.getenv('GEMINI_API_KEY'),
            temperature=0.2,
        )
        tools = await client.get_tools()
        agent = create_react_agent(model=model, tools=tools)

        # Initialize history for this user
        if user_email not in self.conversation_history:
            self.conversation_history[user_email] = []

        # Append user's new message
        self.conversation_history[user_email].append({
            "role": "user",
            "content": prompt
        })

        # Send full conversation to agent
        response = await agent.ainvoke({
            "messages": self.conversation_history[user_email]
        })

        # Extract AI message
        ai_message = response["messages"][-1].content

        # Append AI response to history
        self.conversation_history[user_email].append({
            "role": "ai",
            "content": ai_message
        })

        return ai_message

    async def cleanup_user(self, user_email: str):
        """Remove session and MCP client for a user."""
        if user_email in self.sessions:
            del self.sessions[user_email]
        if user_email in self.clients:
            del self.clients[user_email]




