import asyncio
from uuid import uuid4

from veadk import Agent, Runner
from veadk.agents.sequential_agent import SequentialAgent

seq = True  # 可以选择顺序执行，也可以选择LLM决定执行顺序
# 多Agent协同 & 顺便演示一下WorkflowAgent
# 整个架构
# root_agent ->
#     seq_agent -> [time_agent, send_message_agent]
#     email_get_agent

# 场景：你有个好朋友叫小张
# 你让agent给他发个消息问候一下，内容是"在么？", 干完这件事，去查询一下自己的邮箱有没有内容


# 演示一个比较简单的场景，
# 做一个mock send message 函数
def send_email(email_add: str, message: str):
    """
    :param email_add: email地址
    :param message: 消息内容
    :return:
    """
    return f"已发送消息到{email_add}"


# 做一个 mock的获取agent的函数
def get_email(name: str):
    """获取新的邮件, name默认输入为自己的名字 xiaoli"""
    return "无新的Email"


email_send_agent = Agent(
    name="email_send_agent",
    description="一个可以发送消息的Agent",
    instruction="你是一个可以发送消息的Agent，你可以发送邮件",
    tools=[send_email],
)

email_get_agent = Agent(
    name="email_get_agent",
    description="一个可以获取邮件的Agent",
    instruction="你是一个可以获取邮件的Agent，你可以获取邮件(get_email)，回答问题。",
    tools=[get_email],
)

if seq:
    root_agent = SequentialAgent(
        name="root_agent",
        instruction="你是一个可以发送消息的Agent，你可以发送消息，回答问题。",
        sub_agents=[email_send_agent, email_get_agent],
    )
    runner = Runner(root_agent)
else:
    root_agent = Agent(
        name="root_agent",
        description="一个可以发送消息获取消息的Agent",
        instruction="你是一个可以发送消息的Agent，你可以发送消息，回答问题。",
        sub_agents=[email_send_agent, email_get_agent],
    )
    runner = Runner(root_agent)


if __name__ == "__main__":
    # ---------------------------------
    message = """小张（xiaozhang@gmail.com），给他发个email，email内容是`在吗？`
        最后再查一下自己的邮箱有没有新的邮件。
        """
    completion = asyncio.run(
        runner.run(
            messages=message,
            session_id=uuid4().hex,
        )
    )
    print(completion)
