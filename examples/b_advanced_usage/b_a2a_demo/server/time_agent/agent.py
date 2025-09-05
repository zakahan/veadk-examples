from veadk import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

mcp_tool = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python",
            args=["-m", "mcp_server_time", "--local-timezone=Asia/Shanghai"],
        )
    )
)

agent = Agent(
    name="time_agent",
    description="一个可以获取时间的Agent",
    instruction="你是一个可以获取时间的Agent，你可以获取时间，回答问题。",
    tools=[mcp_tool],
)

root_agent = agent
