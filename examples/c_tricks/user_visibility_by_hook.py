import asyncio
from uuid import uuid4
from typing import Optional

from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
from veadk import Agent, Runner
from veadk.memory.short_term_memory import ShortTermMemory

# 这里做一个简单的演示，演示如何通过callback的方式来提供用户的信息，这里提供的是用户对回答风格的偏好
# 事实上可以通过获取user_id，进而从数据库中获取用户各种信息
# 本脚本演示的是before_model_callback, 需要工具调用的时候也可以通过before_tool_callback来注入用户信息

user_info = {
    "qwerty": "用户偏好严谨翔实的风格",
    "asdfgh": "用户偏好幽默风趣的风格",
    "zxcvbn": "用户偏好简洁明了的风格",
}


def inject_user_info(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    print("[inject_user_info] 修改了system_prompt，加入用户风格偏好")
    ctx = callback_context._invocation_context
    user_id = ctx.user_id
    # 你可以用类似的方式获取其他信息，比如session_id, app_name等
    # app_name = ctx.app_name
    # session_id = ctx.session.id
    # agent_name = ctx.agent.name
    if user_id in user_info:
        llm_request.config.system_instruction += (
            f"\n用户的风格偏好是：{user_info[user_id]}"
        )

    # 我们直接修改system prompt, 注意一定是修改llm_request中的system_prompt，
    # 而不是callback_context._invocation_context中的instruction, 那样是全局修改，会影响到后续的Agent调用"
    print("[inject_user_info] 修改后的system_prompt")
    print(llm_request.config.system_instruction)
    # 注意不要有任何返回值或者返回None即可


agent = Agent(
    name="haiku_master_agent",
    description="一个问答助手",
    instruction="你是一个问答助手，能够根据用户的具体要求来完成工作，注意：关于用户的信息已经存储在各个工具之中了，你直接调用即可，不必提供",
    model_name="doubao-seed-1-6-250615",
    before_model_callback=inject_user_info,
)

short_term_memory = ShortTermMemory()

runner = Runner(
    agent=agent,
    short_term_memory=short_term_memory,
    app_name="an_app",
    user_id="qwerty",
)

if __name__ == "__main__":
    completion = asyncio.run(
        runner.run(
            messages=["如何评价苏轼？"],
            session_id=uuid4().hex,
        )
    )
    print(completion)
