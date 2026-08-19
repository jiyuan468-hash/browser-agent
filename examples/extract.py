"""Example: Extract data from a webpage."""
import asyncio
import sys
from browser_use import Agent, ChatOpenAI


async def extract(url, selector, limit=10):
    task = f'Go to {url}, find all elements matching "{selector}", extract their text, and return up to {limit} results'
    llm = ChatOpenAI(
        model="agnes-2.5-pro",
        api_key="fallback-key",
        base_url="http://127.0.0.1:57321/v1",
        dont_force_structured_output=True,
    )
    agent = Agent(task=task, llm=llm)
    result = await agent.run()
    return result


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extract.py <url> <css-selector> [--limit N]")
        sys.exit(1)
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    asyncio.run(extract(sys.argv[1], sys.argv[2], limit))
