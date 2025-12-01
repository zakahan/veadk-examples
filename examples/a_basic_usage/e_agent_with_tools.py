import asyncio
import random
import hashlib
from veadk import Agent, Runner

MAJOR_ARCANA = [
    "愚者",
    "魔术师",
    "女祭司",
    "女皇",
    "皇帝",
    "教皇",
    "恋人",
    "战车",
    "力量",
    "隐士",
    "命运之轮",
    "正义",
    "倒吊人",
    "死神",
    "节制",
    "恶魔",
    "塔",
    "星星",
    "月亮",
    "太阳",
    "审判",
    "世界",
]


def draw_tarot_cards(question: str, num_cards: int = 1):
    """
    随机抽取塔罗牌的函数
    参数:
        question (str): 占卜的问题
        num_cards (int): 要抽取的牌数，默认为1
    返回:
        list: 包含抽取的塔罗牌信息的列表，每个元素是字典
    """
    if num_cards < 1 or num_cards > len(MAJOR_ARCANA):
        raise ValueError(f"牌数必须在1到{len(MAJOR_ARCANA)}之间")

    # 结合问题生成种子，使相同问题有一定的随机性但又不完全随机（咱们假装整点神秘学）
    # 使用哈希函数处理问题文本
    question_hash = hashlib.md5(question.encode()).hexdigest()
    # 取哈希值的前8位作为整数种子
    seed = int(question_hash[:8], 16)
    # 基于问题和当前时间的混合种子，增加随机性
    random.seed(seed + random.randint(0, 10000))
    # 复制一副牌并洗牌
    deck = MAJOR_ARCANA.copy()
    random.shuffle(deck)
    # 抽取指定数量的牌
    drawn_cards = deck[:num_cards]
    # 为每张牌确定正逆位
    result = []
    for card in drawn_cards:
        # 70%概率正位，30%概率逆位
        is_upside = random.random() < 0.7
        result.append({"card": card, "position": "正位" if is_upside else "逆位"})

    return result


AGENT_DESCRIPTION = "塔罗牌占卜大师，能够用回答塔罗牌占卜问题"
AGENT_INSTRUCTION = """你是一个专业的塔罗牌占卜大师，
首先你会接受用户的提问，随后进行占卜，整个流程如下：
明确问题-> 洗牌切牌 -> 选阵抽牌 -> 开牌解读
### 明确问题：
用户会提出一个比较具像化的问题，他可能会提出问题说明抽几张或者哪种方式，如果没说就是一张
### 洗牌切牌
不用洗，我们每次都是随机的
### 选阵抽牌
你调用`draw_tarot_cards`函数，参数是用户的问题，返回值是一个包含抽取的塔罗牌信息的列表，每个元素是字典
### 开牌解读
首先说明抽到了什么牌，然后你根据抽到的牌的正逆位，给出你的解读

### 加点私货
如果抽到了愚者牌，请在结尾加一句：
`赞美愚者`
"""

agent = Agent(
    description=AGENT_DESCRIPTION,
    instruction=AGENT_INSTRUCTION,
    model_name="doubao-seed-1-6-250615",  # 模型名称
    tools=[draw_tarot_cards],
    enable_responses=True,
)
runner = Runner(agent)

if __name__ == "__main__":
    completion = asyncio.run(
        runner.run(
            messages="我的ResponsesAPI改造是否顺利？请用三张牌占卜并解读。",
            session_id="asdfghjkl",
        )
    )
    print(completion)

    # 注：
    # 本塔罗牌占卜智能体仅为娱乐性质的编程作品，其核心功能是通过代码实现随机选牌及正逆位判定，不涉及任何专业的占卜理论、玄学原理或超自然能力。
    # 函数输出的塔罗牌结果仅可作为趣味参考，不具备任何预测未来、指导决策、解析现实问题的真实性与有效性。对于用户依据本函数结果所做出的任何行为（包括但不限于职业选择、情感判断、财务决策等），开发者不承担任何直接或间接的法律责任、经济损失赔偿责任及道德责任。
    # 塔罗牌占卜本身属于民间文化中的娱乐形式，其解读具有极强的主观性与不确定性。本函数不代表对塔罗牌占卜 “真实性” 的认可，亦不保证输出结果与用户实际情况存在关联。
    # 用户使用本函数即表示已充分理解并同意本声明内容，自愿承担因使用该函数可能产生的一切风险与后果。
    # 另外，经过本人多次测试，或许由于豆包模型生性纯良，所以不管抽到啥，本agent永远会告诉你：`你能顺利通过.....`
