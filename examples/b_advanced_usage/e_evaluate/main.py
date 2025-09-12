import asyncio
import json
import random
import string
from deepeval.metrics import GEval, ToolCorrectnessMetric
from deepeval.test_case import LLMTestCaseParams

from veadk import Agent, Runner
from veadk.config import getenv
from veadk.evaluation.deepeval_evaluator import DeepevalEvaluator
from veadk.memory.short_term_memory import ShortTermMemory
from veadk.tools.demo_tools import get_city_weather
from veadk.prompts.prompt_evaluator import eval_principle_prompt

# 这里的代码基本上是从https://github.com/volcengine/veadk-python/blob/main/veadk_tutorial.ipynb 里copy过来的


def generate_eval_set_id():
    return "".join(
        random.choice(string.ascii_letters + string.digits + "_") for _ in range(6)
    )


app_name = "veadk_playground_app"
user_id = "veadk_playground_user"
session_id = "veadk_playground_session"

agent = Agent(tools=[get_city_weather])
short_term_memory = ShortTermMemory()

runner = Runner(
    agent=agent, short_term_memory=short_term_memory, app_name=app_name, user_id=user_id
)


async def make_eval_set():
    await runner.run(messages="北京的天气怎么样？", session_id=session_id)

    # 调用 runner 中的`save_eval_set`来保存评测集文件到本地
    eval_set_path = await runner.save_eval_set(
        session_id=session_id, eval_set_id=generate_eval_set_id()
    )

    print(f"Evaluation file path: {eval_set_path}")

    with open(eval_set_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"Evaluation file content\n{data}")
    return eval_set_path


async def eval(eval_set_path: str):
    evaluator = DeepevalEvaluator(
        agent=agent, judge_model_api_key=getenv("MODEL_JUDGE_API_KEY")
    )

    judge_model = evaluator.judge_model

    metrics = [
        GEval(
            threshold=0.8,
            name="Base Evaluation",
            criteria=eval_principle_prompt,
            evaluation_params=[
                LLMTestCaseParams.INPUT,
                LLMTestCaseParams.ACTUAL_OUTPUT,
                LLMTestCaseParams.EXPECTED_OUTPUT,
            ],
            model=judge_model,  # 这里需要传入 judge model
        ),
        ToolCorrectnessMetric(threshold=0.5),
    ]
    await evaluator.evaluate(eval_set_file_path=eval_set_path, metrics=metrics)


if __name__ == "__main__":
    eval_set_path = asyncio.run(make_eval_set())
    asyncio.run(eval(eval_set_path))
