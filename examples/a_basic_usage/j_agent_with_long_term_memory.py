import os

os.environ["LOGGING_LEVEL"] = "ERROR"  # noqa
import asyncio
import uuid
from veadk import Agent, Runner
from veadk.memory.long_term_memory import LongTermMemory
from veadk.memory.short_term_memory import ShortTermMemory

# 这里先用local的为例，选local是因为它无持久化也就无代价，方便做演示
# 你可以自己设置其他的backend，比如viking或者是opensearch等等，关于viking后面章节b火山产品部分会专门写一个demo的
ltm = LongTermMemory(
    backend="local",
)
# 短期记忆
stm = ShortTermMemory(
    backend="local",
)

# 定义app_name和user_id
APP_NAME = "chat"
USER_ID = "123"

AGENT_INSTRUCTION = """你可以和用户进行对话。你可以去搜索记忆，但你搜不到就算了，不要觉得记忆里必须要有什么东西，没有就跳过.
除非用户明确说类似`上次和你说的`、`是否记得`这类，否则其他场景别去搜索记忆!
其次，用户问你什么，你就答什么，不要二度询问了，直接一点。
"""
# 创建一个agent
agent = Agent(
    name="chat_agent",
    model_name="doubao-seed-1-6-250615",
    description="你是一个优秀的助手，你可以和用户进行对话。",
    instruction=AGENT_INSTRUCTION,
    long_term_memory=ltm,
)

runner = Runner(
    agent,
    short_term_memory=stm,
    app_name=APP_NAME,
    user_id=USER_ID,
)

# 第一个对话
first_conversation_session_id = str(uuid.uuid4())
message = "你好,能给我讲一讲《三体》里汪淼的故事吗"
completion = asyncio.run(
    runner.run(
        messages=message,
        session_id=first_conversation_session_id,
    )
)
print(f"User:{message}\nAssistant:{completion}\n")


# 对话完毕，讲这段内容加到长期记忆中
# 是的，这里是手动添加，不会让模型自主进行长期记忆添加的
async def add_session_to_memory():
    session = await stm.session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=first_conversation_session_id,
    )
    await ltm.add_session_to_memory(session=session)


asyncio.run(add_session_to_memory())

print("successfully add session to long term memory")

second_conversation_session_id = str(uuid.uuid4())
message = "上次讲到哪个主角了？这次讲下一部的主角吧，大概讲一下。"
completion = asyncio.run(
    runner.run(
        messages=message,
        session_id=second_conversation_session_id,
    )
)
print(f"User:{message}\nAssistant:{completion}\n")
