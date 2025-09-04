import asyncio
import uuid
from veadk import Agent, Runner
from veadk.memory.long_term_memory import LongTermMemory

ltm = LongTermMemory(
    backend="local",
)


agent = Agent(
    name="chat_agent",
    description="你是一个优秀的助手，你可以和用户进行对话。",
    instruction="你可以和用户进行对话。",
    long_term_memory=ltm,
)

runner = Runner(
    agent,
)
# 第一个对话
completion = asyncio.run(
    runner.run(
        messages="你好,我最近在看《三体》，能给我讲一讲汪淼的故事吗",
        session_id=str(uuid.uuid4()),
    )
)
