import os

from google.adk.agents import RunConfig
from google.adk.agents.run_config import StreamingMode
from google.genai import types

os.environ["LOGGING_LEVEL"] = "ERROR"
import asyncio
import uuid
from veadk import Agent, Runner
from veadk.memory.short_term_memory import ShortTermMemory

# 可控参数：（介绍几个比较常见的，更复杂的我懒得找了）
stream = True  # 设置是否流式输出, 在runner.run阶段配置(有两种方式，推荐直接配置入参)
max_llm_calls = (
    5  # 最大调用次数，在runner.run阶段使用，或者可以在config.yaml里配置，默认100
)
temperature = 0.1  # 模型温度，0~1之间，越大越随机
top_p = 0.9  # 模型top_p参数，0~1之间，控制候选词范围（模型会从累积概率达 90% 的候选词中选择。）
thinking_type = "disabled"  # 模型思考类型，关闭模型思考 参考文档：https://www.volcengine.com/docs/82379/1330626
max_tokens = 2048  # 模型最大输出token数

agent = Agent(
    name="chat_agent",  # Agent名称
    description="ChatAgent",  # Agent描述
    instruction="你是一个专业的聊天Agent，能提供各种解答",
    model_name="doubao-seed-1-6-250615",  # 这里建议使用1.6跑本demo，因为有些字段可能1.5不支持
    model_api_base="https://ark.cn-beijing.volces.com/api/v3/",  # 模型的API地址（默认火山方舟平台）
    # model_api_key=os.getenv("ARK_API_KEY"),
    model_extra_config={
        "temperature": temperature,
        "top_p": top_p,
        "extra_body": {"thinking": {"type": thinking_type}},
        "max_tokens": max_tokens,
    },
)

short_term_memory = ShortTermMemory()

runner = Runner(
    agent=agent,  # agent
    short_term_memory=short_term_memory,
    app_name="chat-app",
    user_id="qwerty",
)


async def main():
    # 注意： 由于本脚本需要用到流式输出，而前几个脚本里的run方法是不支持流式的，这里必须采用run_async并采用如下的方式处理
    session_id = uuid.uuid4().hex
    await short_term_memory.session_service.create_session(
        app_name=runner.app_name, user_id=runner.user_id, session_id=session_id
    )
    run_config = RunConfig(
        streaming_mode=StreamingMode.NONE if not stream else StreamingMode.SSE,
        max_llm_calls=max_llm_calls,
    )
    message = types.Content(
        role="user",
        parts=[
            types.Part(text="我已经消化完占卜家序列9魔药了，请问序列8的魔药去哪里搞？")
        ],
    )

    async for event in runner.run_async(
        user_id=runner.user_id,
        session_id=session_id,
        new_message=message,
        run_config=run_config,
    ):
        if event.partial:
            print(event.content.parts[0].text, end="", flush=True)
        # print(event)


if __name__ == "__main__":
    completion = asyncio.run(main())
