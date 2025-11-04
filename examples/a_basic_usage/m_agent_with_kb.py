from uuid import uuid4

import asyncio
from datetime import datetime

from veadk import Agent, Runner
from veadk.knowledgebase import KnowledgeBase

mock_data = [
    """西格蒙德·弗洛伊德（Sigmund Freud，1856年5月6日-1939年9月23日）是精神分析的创始人。
    精神分析既是一种治疗精神疾病的方法，也是一种解释人类行为的理论。弗洛伊德认为，我们童年时期的经历对我们的成年生活有很大的影响，并且塑造了我们的个性。
    例如，源自人们曾经的创伤经历的焦虑感，会隐藏在意识深处，并且可能在成年期间引起精神问题（以神经症的形式）。""",
    """阿尔弗雷德·阿德勒（Alfred Adler，1870年2月7日-1937年5月28日），奥地利精神病学家，人本主义心理学先驱，个体心理学的创始人。
    曾追随弗洛伊德探讨神经症问题，但也是精神分析学派内部第一个反对弗洛伊德的心理学体系的心理学家。
    著有《自卑与超越》《人性的研究》《个体心理学的理论与实践》《自卑与生活》等。""",
]
APP_NAME = "app_name"

# 知识库同样选local 先跑
kb = KnowledgeBase(
    backend="local",
    index="kb_test",  # 有两个可选参数`index`和`app_name`二选一，如果选了app_name，要和agent对应的app_name一致
)

kb.add_from_text(text=mock_data)


def calculate_date_difference(date1: str, date2: str) -> int:
    """
    计算两个日期之间的天数差异
    参数:
        date1: 第一个日期，格式为"YYYY-MM-DD"
        date2: 第二个日期，格式为"YYYY-MM-DD"
    返回:
        两个日期之间的天数差异（绝对值）
    """
    # 解析日期字符串为datetime对象
    try:
        d1 = datetime.strptime(date1, "%Y-%m-%d")
        d2 = datetime.strptime(date2, "%Y-%m-%d")
    except ValueError as e:
        raise ValueError(f"日期格式错误，请使用YYYY-MM-DD格式: {e}")
    # 计算日期差并返回绝对值
    delta = d2 - d1
    return abs(delta.days)


agent = Agent(
    name="chat_agent",
    model_name="doubao-seed-1-6-250615",
    description="你是一个优秀的助手，你可以和用户进行对话。",
    instruction="你是一个优秀的助手，你可以和用户进行对话。",
    knowledgebase=kb,
    tools=[calculate_date_difference],
    model_extra_config={
        "extra_body": {"thinking": {"type": "disable"}},
    },
)


runner = Runner(
    agent,
    app_name=APP_NAME,
)


if __name__ == "__main__":
    completion = asyncio.run(
        runner.run(
            messages="弗洛伊德和阿德勒差了多少岁，多少天？",
            session_id=uuid4().hex,
        )
    )
    print(completion)
