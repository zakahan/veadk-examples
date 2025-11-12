import asyncio
import uuid

from veadk import Agent, Runner
from veadk.memory.short_term_memory import ShortTermMemory

# 本文档展示了如何使用Agent类来创建一个Agent，并详细介绍了主要参数的如何配置。
# 想查看全部参数请直接点开Agent类，有注释
AGENT_DESCRIPTION = "一个专业的俳句大师，任何内容都会使用5-7-5俳句来回答。"
AGENT_INSTRUCTION = "你是一个专业的俳句大师，任何内容都会使用5-7-5俳句来回答。"
agent = Agent(
    name="haiku_master_agent",  # Agent名称
    description=AGENT_DESCRIPTION,  # Agent描述
    instruction=AGENT_INSTRUCTION,  # Agent指令，你可以理解为system-prompt
    model_name="doubao-seed-1-6-250615",  # 模型名称
    model_api_base="https://ark.cn-beijing.volces.com/api/v3/",  # 模型的API地址（默认火山方舟平台）
    # model_api_key=os.getenv("ARK_API_KEY"),  # 模型的API密钥也可以用这种方式
    enable_responses=True,
)

short_term_memory = ShortTermMemory()

runner = Runner(
    agent=agent,  # agent
    short_term_memory=short_term_memory,  # 配置短期记忆
    app_name="haiku-app",
    user_id="qwerty",
)

if __name__ == "__main__":
    completion = asyncio.run(
        runner.run(
            messages="今天吃什么",
            session_id=uuid.uuid4().hex,  # 这个值用来唯一标识本段短期记忆
        )
    )
    print(completion)
    # -----------------------
    # 炊烟袅袅起，
    # 青菜豆腐香满厨。
    # 此味最心安。
