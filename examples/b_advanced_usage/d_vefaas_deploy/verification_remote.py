import argparse
import asyncio
import uuid

from veadk.a2a.remote_ve_agent import RemoteVeAgent
from veadk.memory.short_term_memory import ShortTermMemory
from veadk import Runner

parser = argparse.ArgumentParser(description="Remote VE Agent Runner")
parser.add_argument("--url", required=True, help="The URL of the remote agent")

args = parser.parse_args()
url = args.url
assert url, "Please provide the URL of the remote agent"

client_agent = RemoteVeAgent(name="remote_agent", url=url)


short_term_memory = ShortTermMemory()
runner = Runner(agent=client_agent, short_term_memory=short_term_memory)


if __name__ == "__main__":
    completion = asyncio.run(
        runner.run(
            messages="今天beijing天气如何？",
            session_id=uuid.uuid4().hex,
        )
    )
    print(completion)
