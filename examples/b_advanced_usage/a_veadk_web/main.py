from veadk import Agent
from veadk.tools.builtin_tools.web_search import web_search


APP_NAME = "veadk_web"  # 这个值与文件夹名字保持一致
USER_ID = "user"

root_agent = Agent(
    name="chat_agent",
    description="聊天agent",
    instruction="你可以调用websearch",
    tools=[web_search],
    enable_responses=True,
)
