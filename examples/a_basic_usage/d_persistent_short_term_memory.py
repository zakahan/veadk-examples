import os

os.environ["LOGGING_LEVEL"] = "ERROR"
import asyncio
from veadk import Agent, Runner
from veadk.memory.short_term_memory import ShortTermMemory

app_name = "veadk_playground_app"
user_id = "veadk_playground_user"
session_id = "veadk_playground_session"

agent = Agent()
short_term_memory = ShortTermMemory(
    backend="sqlite",
    local_database_path="./d_persistent_short_term_memory.db",  # sqlite 需要指定数据库路径
    # 如果是 mysql 或 postgresql，需要指定 db_url
    # db_url="mysql://user:password@localhost:3306/db_name"
)  # 可持久化的 short_term_memory，指定 sqlite 后端，对

runner = Runner(
    agent=agent, short_term_memory=short_term_memory, app_name=app_name, user_id=user_id
)
print("======================== 1.1 ========================")

# 同一个会话内，能记住历史记忆
response = asyncio.run(runner.run(messages="我叫VeADK", session_id=session_id))

print(response)
print("======================== 1.2 ========================")
response = asyncio.run(
    runner.run(messages="你还记得我叫什么吗？", session_id=session_id)
)

print(response)

print("======================== 2.1 ========================")
# 模拟服务关闭后，重新启动服务（注意是相同的session_id，只是用这种方式来表示服务关闭了）
# 如果重启short_term_memory，就会丢失历史记忆
short_term_memory = ShortTermMemory(
    backend="sqlite",
    local_database_path="./d_persistent_short_term_memory.db",  #
)
runner = Runner(
    agent=agent, short_term_memory=short_term_memory, app_name=app_name, user_id=user_id
)

response = asyncio.run(
    runner.run(messages="你还记得我叫什么吗？", session_id=session_id)
)

print(response)
