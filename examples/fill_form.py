"""Example: Fill a form on a webpage."""
import asyncio
import json
import sys
from browser_use import Agent, ChatOpenAI


async def fill_form(url, data_file):
    with open(data_file, encoding="utf-8") as fh:
        data = json.load(fh)
    fields = ", ".join(f"{k}={v}" for k, v in data.items())
    task = f"Go to {url} and fill in the form with: {fields}"
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
        print("Usage: python fill_form.py <url> <data.json>")
        sys.exit(1)
    asyncio.run(fill_form(sys.argv[1], sys.argv[2]))
