# Tricks

这部分会零碎的介绍一些veadk的使用技巧，不分先后顺序

| id | 文件名称                    |                描述                | 可用版本*  |
|:---|:------------------------|:--------------------------------:|:------:|
| 01 | user_visibility_by_hook | 让模型/工具过程中可以知道用户信息，这个通过callback实现 | 0.2.12 |
| 02 | custom_agent            |           自定义编排的Agent            | 0.2.12 |

## 详细介绍

### 01. user_visibility_by_hook
由于user_id等参数是在runner中使用的，与agent分离，因此默认情况下，agent所拥有的工具是无状态的，它无法感知到底是谁调用了他，工具只会收到调用的参数。

有一种处理方法是每次提交给llm的时候，都告诉他用户是谁，这样llm调用的时候就知道是谁了，但是这样会导致每次调用大模型都要多传一个信息，非常麻烦。
而且由于大模型幻觉的存在，这种需要完全精准的内容传递是不太现实的。

我们可以通过before_model_callback的方式来实现，具体来说，agent调用model之前，会触发before_model_callback，我们可以在这个回调中，把用户信息传递给model，这样大模型就可以知道是谁调用了他了。
具体实现可见对应脚本


### 02. custom_agent
自定义编排的Agent

veadk提供了LlmAgent和WorkflowAgent（如顺序、并行、循环等），但总是有一些场景，我们希望规划一些流程，但WorkflowAgent又不能满足我们的需求（比如你有一些做判断的分支流程）
那么我们就可以通过自定义Agent来实现

这里以一个Agentic RAG的例子来说明。

- 参考资料：https://google.github.io/adk-docs/agents/custom-agents/