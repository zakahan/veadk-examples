import asyncio
import os
from uuid import uuid4

from veadk import Agent, Runner
from veadk.tools.builtin_tools.web_search import web_search

# veadk有一些内置工具，这里我们以web_search为例

## 请先配置config.yaml里的配置好ak和sk
## 检查ak / sk配置
assert os.getenv("VOLCENGINE_ACCESS_KEY") is not None, "请先配置config.yaml里的ak和sk"
assert os.getenv("VOLCENGINE_SECRET_KEY") is not None, "请先配置config.yaml里的ak和sk"


agent = Agent(
    name="web_search_agent",
    description="一个可以搜索网络的Agent",
    instruction="你是一个可以搜索网络的Agent，你可以搜索网络，回答问题。",
    tools=[web_search],
    enable_responses=True,
)

runner = Runner(agent)


if __name__ == "__main__":
    completion = asyncio.run(
        runner.run(
            messages="介绍一下阿德勒心理学",
            session_id=uuid4().hex,
        )
    )
    print(completion)
