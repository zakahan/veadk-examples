import asyncio
from veadk.a2a.remote_ve_agent import RemoteVeAgent
from veadk.memory.short_term_memory import ShortTermMemory
from veadk import Runner

client_agent = RemoteVeAgent(name="remote_agent", url="http://127.0.0.1:8022")

short_term_memory = ShortTermMemory()
runner = Runner(agent=client_agent, short_term_memory=short_term_memory)


if __name__ == "__main__":
    completion = asyncio.run(
        runner.run(
            messages="现在是北京时间几点？",
            session_id="123",
        )
    )
    print(completion)
