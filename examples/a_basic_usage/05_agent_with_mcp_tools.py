import asyncio
from veadk import Agent, Runner
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

# uv add mcp_server_time
# 本脚本展示如何使用MCPTool，简洁起见，这里采用了第三方库 time-mcp-server(stdio),方便我们直接使用，不用自己写了
# https://github.com/modelcontextprotocol/servers/tree/main/src/time


# mcptool (你可以理解为这是一个mcp的client），它会连接到一个mcp server，然后作为tools提供给agent使用
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

runner = Runner(agent)


if __name__ == "__main__":
    completion = asyncio.run(
        runner.run(
            messages="现在悉尼时间是多少？",
            session_id="asdfghjkl",
        )
    )
    print(completion)
