import os
from uuid import uuid4

os.environ["LOGGING_LEVEL"] = "ERROR"  # noqa
from veadk import Agent, Runner
from veadk.memory.short_term_memory import ShortTermMemory

# 由于这里需要在Terminal里演示如何进行对话，所以建议提前配置好logging level 为ERROR，这样就比较好。
# config.yaml
# ```yaml
# logging:
#   level: ERROR
# ```

# 本脚本会演示如何使用agent进行多轮对话，并且实现了一个简单的多轮对话demo

agent = Agent(
    name="chat_agent",
    description="你是一个优秀的助手，你可以和用户进行对话。",
    instruction="不管用户说什么，你在回答的开头都要带上`你好`，然后再回答用户的问题。",
    enable_responses=True,
)


short_term_memory = ShortTermMemory(backend="local")

runner = Runner(
    agent,
    short_term_memory=short_term_memory,  # 维护多轮对话的关键（当然你单轮对话也要设置这东西其实）
)

session_id = uuid4().hex


# 整一个简单的多轮对话demo，具体内容自己玩哈
async def main():
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            break
        completion = await runner.run(
            messages=user_input,
            session_id=session_id,
        )
        print(f"Assistant: {completion}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
