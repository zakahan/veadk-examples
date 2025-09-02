# Basic-Usage

这部分介绍的是最基础的用法，包括工具调用，长期记忆、短期记忆以及流失输出等基础使用方式，不会涉及到更复杂的部分。

> 注1:可用版本指的是**该example在当前版本范围内测试过且能够跑通**，其他版本没有测试过故无法保证，说不定也能跑。
> 
> 注2:顺序并不表示难度

| id | 文件名                                  |          描述           | 可用版本* |
|:---|:-------------------------------------|:---------------------:|:---:|
| 01 | 01_tiny_agent_usage.py               |      超简洁的Agent用法      | 0.2.5 |
| 02 | 02_detail_agent_usage.py             |     详细描述的单Agent用法     | 0.2.5 |
| 03 | 03_agent_with_tools.py               |     带工具调用的Agent用法     | 0.2.5 |
| 04 | 04_agent_with_builtin_tools.py       |     使用内置工具的Agent      | 0.2.5 |
| 05 | 05_agent_with_mcp_tools.py           |     使用mcp工具的Agent     | 0.2.5 |
| 06 | 06_agent_with_multi_turn_dialogue.py |      带多轮对话的Agent      | 0.2.5 |
| 07 | 07_multi_modal.py                    | 多模态Agent(输入为图片&输出为图片) | 0.2.5|
| 08 | 08_agent_with_long_term_memory.py    |      带长期记忆的Agent      | 0.2.5 |
| 09 | 09_agent_with_kb.py                  |      带知识库的Agent       | 0.2.5 |
| 10 | 10_multiple_agents.py                |        多Agent         | 0.2.5 |
| 11 | 11_agent_stream_chat.py              |         流式输出          | 0.2.5 |
| 12 | 12_complex_agent.py                  |  综上所有能力复合的一个Agent案例   | 0.2.5 |



## 详细介绍

### 01_tiny_agent_usage.py


这是一个非常简单的Agent用法，核心部分其实只有两行
```python
agent = Agent()
runner = Runner(agent)
```
如果你配置好了config.yaml,只需要分别定义了Agent与Runner，并且使用asynico启动runner的run函数即可。
- [可以看这个文档](https://volcengine.github.io/veadk-python/introduction.html#agent)

### 02_detail_agent_usage.py

该部分介绍了Agent的详细用法，说明了如何配置Agent相关的一些基础参数，包括api-key、api-base以及系统提示词等（instruction）


### 03_agent_with_tools.py

作为一个agent，怎么能没有可以调用的工具呢？
这部分介绍了如何使用agent调用工具（当然这部分仅仅展示了如何调用function工具，实际上agent还支持mcp工具类型）


### 04_agent_with_builtin_tools.py

- [关于内置工具的文档](https://volcengine.github.io/veadk-python/tool.html#%E5%86%85%E7%BD%AE%E5%B7%A5%E5%85%B7)

veadk存在一些内置的工具，你可以直接使用，不需要自己去实现。
只需要在config.yaml里添加新的配置即可。由于后续还会有很多很多的新的配置内容，所以我还写（抄）了一个全内容的`config.yaml.full`

其次，很多内置工具或内置的能力与火山引擎其他产品有关，所以你需要去对应的网址申请开通等等
这里可以从`veadk-python`的官方文档去看看对应的功能是否需要开通，在哪里开通：
- [内置功能介绍以及对应文档](https://volcengine.github.io/veadk-python/introduction.html)

比如`web_search`功能
![web_search](images/img-04-a.png)

运行本脚本可以发现日志里存在function-call的内容，说明成功调用了web-search工具。
![web_search](images/img-04-b.png)

### 05_agent_with_mcp_tools.py

这是一个使用mcp工具的例子。
tools(client)部分依靠mcp库和google-adk的mcp-toolset实现。
而mcp server部分依靠第三方库`mcp_server_time`实现，作为演示。所以必须事先安装`mcp_server_time`
```bash
uv add mcp_server_time
```


### 06_agent_with_multi_turn_dialogue.py

这是一个多轮对话的案例，其实对veadk做多轮对话并不复杂。
实现veadk多轮对话的关键在于ShortTermMemory。