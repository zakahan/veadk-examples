from time_agent.agent import agent  # type: ignore

from veadk.memory.short_term_memory import ShortTermMemory
from veadk.types import AgentRunConfig

# [required] instantiate the agent run configuration
agent_run_config = AgentRunConfig(
    app_name="time-agent",
    agent=agent,  # type: ignore
    short_term_memory=ShortTermMemory(backend="local"),  # type: ignore
)
