# agent.py
import asyncio
from constants import composio
from langchain_mcp_adapters.client import MultiServerMCPClient

class GoogleWorkspaceCopilot:
    """
    AI Agent for Google Workspace using Composio Tool Router and LangChain MCP client.
    Toolkits: Gmail, Docs, Sheets, Presentation
    """

    def __init__(self):
        self.sessions = {}  # user_id -> session info
        self.clients = {}   # user_id -> MultiServerMCPClient

    async def create_session_for_user(self, user_email: str) -> str:
        """Create a Tool Router session for a user if it doesn't exist."""
        if user_email in self.sessions:
            return self.sessions[user_email]['url']

        session = self.composio.experimental.tool_router.create_session(
            user_id=user_email,
            toolkits=[
                {'toolkit': 'gmail'}
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
                "tool_router": {
                    "url": mcp_url,
                    "transport": "streamable_http"  # recommended transport
                }
            }
        )
        self.clients[user_email] = client
        return client

    async def run_command(self, user_email: str, prompt: str):
        """Run a natural language command via MCP client."""
        client = await self.setup_mcp_client(user_email)
        try:
            response = await client.run(prompt)
            return response
        except Exception as e:
            return f"Error executing command: {e}"

    async def cleanup_user(self, user_email: str):
        """Remove session and MCP client for a user."""
        if user_email in self.sessions:
            del self.sessions[user_email]
        if user_email in self.clients:
            del self.clients[user_email]


# -----------------------
# Example CLI usage
# -----------------------
async def main():
    user_email = "devanshbansal2021@gmail.com"
    agent = GoogleWorkspaceCopilot()

    print("Google Workspace Copilot CLI")
    print("Type 'exit' to quit.\n")

    while True:
        prompt = input("Enter a command: ")
        if prompt.lower() == "exit":
            print("Exiting...")
            break

        response = await agent.run_command(user_email, prompt)
        print("Response:", response)

    await agent.cleanup_user(user_email)


if __name__ == "__main__":
    asyncio.run(main())
