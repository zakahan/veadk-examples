import asyncio
import os
from uuid import uuid4

from veadk import Agent, Runner
from veadk.tools.builtin_tools.image_generate import image_generate
from veadk.types import MediaMessage


assert os.getenv("MODEL_IMAGE_API_KEY") is not None, (
    "请设置config里的image部分，不然没办法生成图片嗷！（对了记得开通模型）"
)

# 上一个demo玩过了多agent，那么咱们这次就来整一个玩玩多模态的agent吧！
# 先整一个图片理解 （input image&text | output text）
iu_agent = Agent(
    name="ImageUnderstander",
    model_name="doubao-seed-1-6-250615",  # 1.5只有文本模态，所以这里只能用1.6，下面也同理
    description="一个能理解图片的Agent",
    instruction="你是一个图像理解Agent。你能够理解图像并返回图像的文字描述。",
    enable_responses=True,
)

# 再整一个图片生成的（input text | output image&text)
ig_agent = Agent(
    name="ImageGenerator",
    model_name="doubao-seed-1-6-250615",  # 这里可以用1.5,因为生成依靠的是工具
    description="一个能生成图片的Agent",
    instruction="你是一个图像生成Agent。你能够根据文字描述生成图像。",
    tools=[image_generate],
    enable_responses=True,
)

# 然后整一个root agent，用来控制整个流程（诶，合起来就是 image in image out了）
root_agent = Agent(
    model_name="doubao-seed-1-6-250615",
    name="RootAgent",
    description="一个多模态Agent",
    instruction="你拥有两个子Agent，分别是图片理解的Agent和图片生成的Agent，你可以根据用户的输入和输出分别处理不同的任务。",
    sub_agents=[iu_agent, ig_agent],
    enable_responses=True,
)

runner = Runner(root_agent)


if __name__ == "__main__":
    # 带图片的输入需要使用`MediaMessage`
    local_path = os.path.join(os.path.dirname(__file__), "images", "example-data.png")
    messages = [
        MediaMessage(
            text="请描述这张图片",
            media=local_path,
        ),
        "你描述的真好，能不能根据这个文字描述生成一张类似的图片呢？（不要水印）",
    ]
    session_id = uuid4().hex
    for message in messages:
        print(f"User: {message}")
        completion = asyncio.run(
            runner.run(
                messages=message,
                session_id=session_id,
            )
        )
        print(completion)
