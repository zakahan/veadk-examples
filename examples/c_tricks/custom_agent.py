import asyncio
import json
from uuid import uuid4
from typing import AsyncGenerator, TypeAlias, Literal

from anthropic import BaseModel
from google.adk.agents import BaseAgent, InvocationContext
from google.adk.events import Event
from google.genai.types import Content, Part
from pydantic import Field
from typing_extensions import override
from veadk import Agent, Runner
from veadk.knowledgebase import KnowledgeBase

DEFAULT_TOP_K = 5

_StrategyAlias: TypeAlias = Literal[
    "direct_answer",
    "search_knowledgebase",
]


class RetrievalStrategyModel(BaseModel):
    """
    Retrieval Strategy
    output_schema of retrieval_strategy_agent
    """

    strategy: _StrategyAlias = Field(
        ...,
        description="The strategy to use for retrieval. Options are: 'keyword', 'semantic'",
    )
    query: str = Field(
        ...,
        description="The query to use for retrieval. This is the original query from the user or the new query.",
    )


strategy_agent = Agent(
    name="retrieval_strategy_agent",
    model_name="doubao-seed-1-6-250615",
    description="这是一个检索策略选择Agent，用来判断是否需要检索检索",
    instruction="你是一个检索策略选择智能体，你属于`阿罗德斯`的一部分，你会收到一些用户提问，你需要判断是否需要检索知识库。如果你认为这是一个比较大众常规的问题，"
    + "那没有必要检索知识库，直接回答即可。如果需要检索知识库，则选择search_knowledgebase。不管是哪种策略，都要重新生成问题。"
    + "问题需要更加的翔实",
    model_extra_config={
        "extra_body": {"thinking": {"type": "disabled"}},
    },
    output_schema=RetrievalStrategyModel,  # 对应openai api中的response_format，这是一种结构化输出的技巧，比直接prompt说明更推荐
)


generate_agent = Agent(
    name="generate_agent",
    model_name="doubao-seed-1-6-250615",
    description="这是一个生成回答的Agent，用来生成最终的回答",
    instruction="你是一个内容生成智能体，你属于`阿罗德斯`的一部分，你会收到一些用户提问，你需要根据用户的提问和检索到的知识来生成最终的回答。"
    + "如果没有检索到知识，则直接回答即可。",
)


class RetrievalExecutionAgent(BaseAgent):
    retrieval_strategy_agent: Agent  # 用来提供检索策略参考
    kb: KnowledgeBase  # 知识库
    generate_agent: Agent  # 用来生成最终回答的agent
    # model_config allows setting Pydantic configurations if needed, e.g., arbitrary_types_allowed
    model_config = {"arbitrary_types_allowed": True}

    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        # step1 : 调用检索策略智能体，决定是否需要检索
        async for event in self.retrieval_strategy_agent.run_async(ctx):
            if event.is_final_response():
                yield event

        # step2: 判断是否需要检索，需要则进行检索
        strategy = json.loads(ctx.session.events[-1].content.parts[0].text)
        generate_info = {"query": strategy["query"]}

        if strategy["strategy"] == "search_knowledgebase":
            chunks = self.kb.search(strategy["query"])
            generate_info["chunks"] = [chunk.content for chunk in chunks]
        else:
            generate_info["chunks"] = []
        yield Event(
            invocation_id=ctx.invocation_id,
            author="KnowledgeBaseAgent",
            content=Content(
                parts=[
                    Part(
                        text=json.dumps(generate_info, ensure_ascii=False),
                    )
                ],
                role="model",
            ),
        )

        # step3: 生成结果
        async for event in self.generate_agent.run_async(ctx):
            yield event


if __name__ == "__main__":
    kb = KnowledgeBase(
        backend="local",
        index="kb_test",
    )

    kb.add_from_text(
        text=[
            "霍纳奇斯山脉主峰藏着安提格努斯家族宝藏，可以搞到占卜家序列4的魔药。",
            "查拉图疯了，但是他肯定有占卜家序列4的魔药配方",
            "贝克兰德的圣塞缪尔教堂查尼斯门后面有安提格努斯家族笔记，可以搞到占卜家序列4的魔药。",
        ]
    )

    retrieval_agent = RetrievalExecutionAgent(
        name="retrieval_agent",
        description="这是一个检索执行Agent，用来执行检索和生成回答",
        retrieval_strategy_agent=strategy_agent,
        kb=kb,
        generate_agent=generate_agent,
    )

    runner = Runner(
        retrieval_agent,
        app_name="retrieval_app",
    )
    # 执行
    completion = asyncio.run(
        runner.run(
            messages="阿罗德斯，你知道去哪里能搞到占卜家序列4诡法师的魔药？",
            session_id=uuid4().hex,
        )
    )
    print(completion)
