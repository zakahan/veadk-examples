# Advanced-Usage

包括veadk-web的使用，a2a协议使用、apmplus/cozeloop上的可观测监控，vefaas上的部署、Agent评估，prompt_pilot实现prompt优化等等。

> 注1:可用版本指的是**该example在当前版本范围内测试过且能够跑通**，其他版本没有测试过故无法保证，说不定也能跑。
> 
> 注2:顺序并不表示难度

| id | 目录名称                 |               描述               | 可用版本* |
|:---|:---------------------|:------------------------------:|:---:|
| 01 | a_veadk_web          |         如何使用veadk-web          | 0.2.5 |
| 02 | b_a2a_demo           |           a2a协议的简单使用           | 0.2.5 |
| 03 | c_observability      |         agent应用与可观测平台          | 0.2.5 |
| 04 | d_vefaas_deploy      |        在vefaas上部署agent         | 0.2.5 |
| 05 | e_evaluate           |            agent评估             | 0.2.5 |
| 06 | f_prompt_pilot       |        agent的prompt 优化         | 0.2.5 |

## 详细介绍

### 01. a_veadk_web

一个简要的demo，展示了如何使用veadk_web。
```bash
cd examples/b_advanced_usage

# 启动
veadk web --host 0.0.0.0
# 如果需要使用长期记忆，请先配置环境变量，比如`local`模式
# LONG_TERM_MEMORY_BACKEND=local veadk web

# 进入 http://0.0.0.0:8000查看
# windows端如果看不到可以切换到 http://localhost:8000
```

![veadk-web-2](images/veadk_web.png)

### 02. b_a2a_demo

这个demo用来简要的演示a2a服务。

- 启动服务端
```bash
cd b_advanced_usage/b_a2a_demo 

python server/server.py
```

- 启动客户端
```bash
cd b_advanced_usage/b_a2a_demo 

python client.py
```



- 关于a2a协议，更多的信息可以参考以下链接

https://github.com/a2aproject/a2a-python

https://a2a-protocol.org/latest/



- 另外启动server之后，可以通过

http://localhost:8022/.well-known/agent-card.json

来查看agent-card.json的信息



对于a2a协议，你可以大致理解为：我们肯定有需求，需要将一些agent部署到某个平台，在本地通过另一些agent调用，实现两个agent之间的沟通，那么这个沟通的协议是什么？a2a。

当然你可以使用其他的协议来完成这个事情，比如mcp协议（这里埋个伏笔，因为veadk后面也做了），但a2a是一个更推荐的选择。



### 03. c_observability







### 04. d_vefaas_deploy

### 05. e_evaluate

### 06. f_prompt_pilot

