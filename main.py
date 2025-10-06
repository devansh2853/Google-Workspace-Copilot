from core.constants import composio
import sys
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

async def create_tool_router_session(user_email):
    session = composio.experimental.tool_router.create_session(
            user_id=user_email,
            toolkits=[
                {'toolkit': 'gmail'}
            ],
        )
    # session = composio.experimental.tool_router.create_session(user_id=user_email)
    return session['url']

async def setup_mcp_client(user_email: str) -> MultiServerMCPClient:
        """Set up LangChain MCP client for a user."""

        mcp_url = await create_tool_router_session(user_email)
        client = MultiServerMCPClient(
            {
                "tool_router": {
                    "url": mcp_url,
                    "transport": "streamable_http"  # recommended transport
                }
            }
        )
        return client
async def main():

    # mcp_url = create_tool_router_session("devanshbansal2021@gmail.com")
    client = await setup_mcp_client("devanshbansal2021@gmail.com")
    tools = await client.get_tools()
    print(tools)
    

if __name__ == "__main__":
    asyncio.run(main())