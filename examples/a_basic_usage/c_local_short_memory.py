import os

os.environ["LOGGING_LEVEL"] = "ERROR"
import asyncio
from veadk import Agent, Runner
from veadk.memory.short_term_memory import ShortTermMemory

app_name = "veadk_playground_app"
user_id = "veadk_playground_user"
session_id = "veadk_playground_session"

agent = Agent(enable_responses=True)
short_term_memory = ShortTermMemory(
    backend="local"
)  # 指定 local 后端，或直接 ShortTermMemory()

runner = Runner(
    agent=agent, short_term_memory=short_term_memory, app_name=app_name, user_id=user_id
)
print("======================== 1.1 (预期行为：给出回应）========================")

# 同一个会话内，能记住历史记忆
response = asyncio.run(runner.run(messages="我叫李华", session_id=session_id))

print(response)
print("======================== 1.2 (预期行为：记得名字）========================")
response = asyncio.run(
    runner.run(messages="你还记得我叫什么吗？", session_id=session_id)
)

print(response)

print("======================== 2.1 (期待行为：不记得名字）========================")
# 模拟服务关闭后，重新启动服务（注意是相同的session_id，只是用这种方式来表示服务关闭了）
# 如果重启short_term_memory，就会丢失历史记忆
short_term_memory = ShortTermMemory(backend="local")
runner = Runner(
    agent=agent, short_term_memory=short_term_memory, app_name=app_name, user_id=user_id
)

response = asyncio.run(
    runner.run(messages="你还记得我叫什么吗？", session_id=session_id)
)

print(response)
