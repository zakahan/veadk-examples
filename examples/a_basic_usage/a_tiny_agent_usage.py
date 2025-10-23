import asyncio
from uuid import uuid4

from veadk import Agent, Runner

# 请保证你已经拥有了config.yaml，并且设置好了api_key

agent = Agent()
runner = Runner(agent)

if __name__ == "__main__":
    completion = asyncio.run(runner.run(messages="你好", session_id=uuid4().hex))
    print(completion)
