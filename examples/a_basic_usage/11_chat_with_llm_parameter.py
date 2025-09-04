import os

os.environ["LOGGING_LEVEL"] = "ERROR"  # noqa
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

os.environ["MODEL_AGENT_MAX_LLM_CALLS"] = str(max_llm_calls)
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


if __name__ == "__main__":
    completion = asyncio.run(
        runner.run(
            messages="今天吃什么",
            session_id=str(uuid.uuid4()),
            stream=stream,
        )
    )
    # print(completion)
