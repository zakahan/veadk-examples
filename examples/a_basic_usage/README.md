# Basic-Usage

这部分介绍的是最基础的用法，包括工具调用，长期记忆、短期记忆以及流失输出等基础使用方式，不会涉及到更复杂的部分。

> 注1:可用版本指的是**该example在当前版本范围内测试过且能够跑通**，其他版本没有测试过故无法保证
> 
> 注2:顺序并不表示难度

| id | 文件名                                  |          描述           | 可用版本* |
|:---|:-------------------------------------|:---------------------:|:---:|
| 01 | 01_tiny_agent_usage.py               |      超简洁的Agent用法      | 0.2.5 |
| 02 | 02_detail_agent_usage.py             |     详细描述的单Agent用法     | 0.2.5 |
| 03 | 03_agent_with_tools.py               |     带工具调用的Agent用法     | 0.2.5 |
| 04 | 04_agent_with_builtin_tools.py       |     使用内置工具的Agent      | 0.2.5 |
| 05 | 05_agent_with_multi_turn_dialogue.py |      带多轮对话的Agent      | 0.2.5 |
| 06 | 06_multi_modal.py                    | 多模态Agent(输入为图片&输出为图片) | 0.2.5|
| 07 | 07_agent_with_long_term_memory.py    |      带长期记忆的Agent      | 0.2.5 |
| 08 | 08_agent_with_kb.py                  |      带知识库的Agent       | 0.2.5 |
| 09 | 09_multiple_agents.py                |        多Agent         | 0.2.5 |
| 10 | 10_agent_stream_chat.py              |         流式输出          | 0.2.5 |
| 11 | 11_complex_agent.py                  |  综上所有能力复合的一个Agent案例   | 0.2.5 |



## 详细介绍

### 01_tiny_agent_usage.py

这是一个非常简单的Agent用法，核心部分其实只有两行
```python
agent = Agent()
runner = Runner(agent)
```
如果你配置好了config.yaml,只需要分别定义了Agent与Runner，并且使用asynico启动runner的run函数即可。