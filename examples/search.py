"""Example: Search the web and summarize results."""
import asyncio
import sys
from browser_use import Agent, ChatOpenAI


async def search_web(query, top_n=5):
    llm = ChatOpenAI(
        model="agnes-2.5-pro",
        api_key="fallback-key",
        base_url="http://127.0.0.1:57321/v1",
        dont_force_structured_output=True,
    )
    task = f'Search for "{query}" and summarize the top {top_n} results'
    agent = Agent(task=task, llm=llm)
    result = await agent.run()
    return result


if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "browser use python"
    print(f"Searching for: {query}")
    result = asyncio.run(search_web(query))
    print(result)
