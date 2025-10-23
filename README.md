### 来都来了

同学你好👋，你是来开发agent的吗？你听说过`veadk-python`么？

- 你想知道如何快速开发agent么？
- 你想了解agent怎么部署、评测、怎么实现搜索、调用mcp之类的功能吗？

那你是问对人了

来都来了、都是哥/姐们、给个面子，耽误你两分钟看一看`veadk-python`的使用教程好吗（不保证是保姆级）：

**声明**：
1. 本仓库为非官方使用教程，如有更新或其他原因导致本仓库某代码失效请以官方文档和官方仓库为准。
2. 本人日常摆烂人格，经常写着写着就查无此人了，所以说不准哪天就不更新了，不要太对我抱有期望，提前向各位道歉。
3. 本人不是很会写文档，而且习惯`注释直通大脑，文档充当草稿`，所以可能有一大堆没啥用的注释以及比较乱的文档内容，请见谅，遇到不清楚不合理的描述内容之类的请提一下issue说说，我会改的。

- [veadk-python](https://github.com/volcengine/veadk-python)
- [veadk官方文档](https://volcengine.github.io/veadk-python)

### 写在开头

1. 本项目全程使用uv进行环境管理，所以建议你也使用uv来。这里是uv的配置方式:[how-to-install-uv](github.com/volcengine/veadk-python?tab=readme-ov-file)
2. veadk所有key的配置都依赖`config.yaml`（其实也可以用环境变量），所以希望你牢牢记得，别把这东西泄露出去。
3. 代码运行的目录为项目根目录，因为`config.yaml`在这里（所以说如果你想在其他地方运行，那么里面要有`config.yaml`或配置的环境变量）

#### 配置依赖与api-key

这些都是必须的，你需要自己去申请与配置。
1. api-key申请：
   1. 请前往[火山方舟平台](https://console.volcengine.com/ark/)申请api-key（或者其他符合openai-api规范的模型平台）
   2. 留着这东西，等下copy到config.yaml里

2. clone项目并配置python环境
```bash
# clone
git clone https://github.com/zakahan/veadk-examples.git
cd veadk-examples

# 安装依赖（一口气全安装）
uv sync

# 激活环境
# mac or linux
source .venv/bin/activate
# windows
.\.venv\Scripts\activate
```

3. 添加config.yaml，配置需要的依赖
```bash
cp config.yaml.example config.yaml

# 修改config.yaml第6行 ，将第一步申请到的api-key添加到这里
```
目前你只配置了最基础的key，剩下的key会在每个example里逐一介绍（不然一次性介绍挨个申请你可能比较累，你也不一定要用）


### 项目结构

> 本项目是由一堆example组成的，每个example下面的子目录都可以单独运行，并且都有各自的README文件来介绍如何运行。有任何问题请直接点开对应的README来查看。

- 章节a: `a_basic_usage`: 基础使用案例，包括单/多个Agent的运行，带工具(mcp)、多轮对话，流式输出，多模态、长期记忆和知识库等等，如果你仅仅是想要娱乐的方式来“玩”Agent，那么这些就足够了。
- 章节b: `b_advanced_usage`: 进阶使用案例，包括veadk-web的使用，a2a协议使用、apmplus/cozeloop上的可观测监控，vefaas上的部署、Agent评估，prompt_pilot实现prompt优化等等。
- 章节c: `c_tricks`： 技巧性用法，一些对veadk做复杂处理需要的技巧，比如如何让tool调用不再是无状态，而是能识别用户身份等，或者是一些自定义的用法，这些可能在google-adk文档中有说明，会补充过来。
- 章节d: `d_demohouse`: 一些很具体的demo，这些demo也不会很复杂，往往是一个个的案例。

### 阅读顺序

进入您想查看的章节，然后先阅读readme，再阅读对应的代码，代码+注释+readme文档=总体使用教程。

### 项目目标

1. 足够基础、足够详细：我会尽可能将基础使用的example写的都足够的简单，能帮你快速上手，尽可能覆盖足够的基础使用方案，对于新手容易触发的错误，尽可能给出提示。
2. 足够专业、足够简单：我会尽可能将一些复杂案例写的专业且标准，同时也会尽可能将复杂的问题简单化，也尽可能的具体化。