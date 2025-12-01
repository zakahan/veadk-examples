import os
import uuid

os.environ["LOGGING_LEVEL"] = "ERROR"
import asyncio
from veadk import Agent, Runner
from veadk.memory.short_term_memory import ShortTermMemory

app_name = "veadk_playground_app"
user_id = "veadk_playground_user"
session_id = uuid.uuid4().hex

agent = Agent(enable_responses=True)
short_term_memory = ShortTermMemory(
    backend="sqlite",
    local_database_path="./d_persistent_short_term_memory.db",  # sqlite 需要指定数据库路径
    # 如果是 mysql 或 postgresql: 1. backend切换到mysql或者postgresql，2. 直接指定db_url
)  # 可持久化的 short_term_memory，指定 sqlite 后端，对

# # mysql
# # 方案1: 直接指定db_url
# short_term_memory = ShortTermMemory(
#     db_url="mysql://username:password@host:port/database"     # The `db_url` is set, ignore `backend` option.
# )
#
# # 方案2: 指定backend 并在config.yaml里做配置
# ```yaml
# database:
#   mysql:
#     host: x.x.x.x
#     user: username
#     password: password
#     database: database_name
#     charset: utf8mb4
# ```
# short_term_memory = ShortTermMemory(
#     backend="mysql",
# )

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

print("======================== 2.1  (预期行为：记得名字）========================")
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
