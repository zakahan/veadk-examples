import os
import json
import asyncio
from veadk import Agent, Runner
from veadk.tracing.telemetry.exporters.cozeloop_exporter import CozeloopExporter
from veadk.memory.short_term_memory import ShortTermMemory
from veadk.tools.demo_tools import get_city_weather
from veadk.tracing.telemetry.opentelemetry_tracer import OpentelemetryTracer

app_name = "veadk_playground_app"
user_id = "veadk_playground_user"
session_id = "veadk_playground_session"


# 请先配置好cozeloop部分的config.yaml
# observability:
#   opentelemetry:
#     cozeloop:
#       endpoint: https://api.coze.cn/v1/loop/opentelemetry/v1/traces
#       api_key:
#       service_name: # Coze loop `space_id`

assert os.getenv("OBSERVABILITY_OPENTELEMETRY_COZELOOP_SERVICE_NAME") is not None, (
    "Please set OBSERVABILITY_OPENTELEMETRY_COZELOOP_SERVICE_NAME in your environment variables"
)
assert os.getenv("OBSERVABILITY_OPENTELEMETRY_COZELOOP_ENDPOINT") is not None, (
    "Please set OBSERVABILITY_OPENTELEMETRY_COZELOOP_ENDPOINT in your environment variables"
)
assert os.getenv("OBSERVABILITY_OPENTELEMETRY_COZELOOP_API_KEY") is not None, (
    "Please set OBSERVABILITY_OPENTELEMETRY_COZELOOP_API_KEY in your environment variables"
)

exporters = [CozeloopExporter()]  # 初始化 tracing 上报器

tracer = OpentelemetryTracer(exporters=exporters)

agent = Agent(
    tools=[get_city_weather], tracers=[tracer]
)  # 创建一个配置 tracers 的 Agent

short_term_memory = ShortTermMemory()

runner = Runner(
    agent=agent, short_term_memory=short_term_memory, app_name=app_name, user_id=user_id
)

# 如果在 agent 中设置了tracer，
# 并且在 `run` 中指定保存，runner将会尝试保存 tracing 文件
asyncio.run(
    runner.run(
        messages="北京的天气怎么样？", session_id=session_id, save_tracing_data=True
    )
)

print(f"Tracing file path: {tracer._trace_file_path}")

with open(tracer._trace_file_path, "r") as f:
    tracing_content = f.read()

print(
    f"Tracing file content:\n{json.dumps(json.loads(tracing_content), indent=2, ensure_ascii=False)}"
)
