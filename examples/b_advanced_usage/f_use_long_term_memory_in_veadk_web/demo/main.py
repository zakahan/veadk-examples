import asyncio

from google.adk.events import Event
from google.adk.sessions import Session
from google.genai.types import Content, Part
from veadk import Agent
from veadk.memory.long_term_memory import LongTermMemory


ltm = LongTermMemory(backend="local", app_name="chat", user_id="user")


# 加条历史记忆
async def add_fake_history():
    session = Session(
        id="b24909c3-1256-4766-9e77-881cd7f429a2",
        app_name="chat",
        user_id="user",
        state={},
        events=[
            Event(
                content=Content(
                    parts=[
                        Part(text="你好,能给我讲一讲《三体》里汪淼的故事吗"),
                    ],
                    role="user",
                ),
                author="user",
            ),
            Event(
                content=Content(
                    parts=[
                        Part(
                            text="""《三体》中，汪淼是一位顶尖的纳米材料科学家，他的故事是串联起地球文明与三体文明首次接触的关键线索。  
    起初，他因“科学边界”组织成员的自杀事件被警方注意，随后经历了一系列诡异现象：眼前频繁出现倒计时数字，拍摄的照片中也存在无法解释的倒计时，甚至在天文观测中，宇宙背景辐射的闪烁也呈现出倒计时规律。这些超自然体验让他陷入巨大的精神压力，几乎怀疑自己的科学信仰。  
    在刑警史强的介入下，汪淼接触到“三体”虚拟现实游戏，通过游戏中的文明轮回，逐渐意识到这并非普通游戏，而是外星文明（三体人）对地球的试探与预警。他发现“科学边界”的学者们因得知“物理学不存在”的真相而崩溃，而这一切的幕后推手，正是早已与三体文明建立联系的叶文洁。  
    汪淼的纳米材料技术成为对抗三体的关键。他研发的“飞刃”（高强度纳米丝）被应用于“古筝行动”——在巴拿马运河上空架设纳米丝组成的“切割网”，成功截获了三体文明发送给地球叛军的信息，揭露了三体舰队正在入侵地球的真相。  
    尽管汪淼在后续故事中出场较少，但他的科学能力与冷静判断力，为人类早期对抗三体危机提供了重要支撑，也象征着理性与科学在面对未知恐惧时的坚守。"""
                        ),
                    ],
                    role="model",
                ),
                author="chat_agent",
            ),
        ],
    )
    await ltm.add_session_to_memory(session=session)


loop = asyncio.get_event_loop()
# 将异步任务提交到循环中，由外部循环调度执行
loop.create_task(add_fake_history())


root_agent = Agent(name="chat_agent", description="聊天agent", long_term_memory=ltm)
