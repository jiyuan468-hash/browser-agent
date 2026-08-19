"""CLI entry point for BrowserAgent."""
import asyncio
import argparse
import sys
from browser_agent.config import AgentConfig


def main():
    parser = argparse.ArgumentParser(prog="browser-agent", description="AI-powered browser automation agent")
    parser.add_argument("--config", default=None, help="Path to config YAML file")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    subparsers = parser.add_subparsers(dest="command", required=True)

    sp = subparsers.add_parser("search", help="Search the web and summarize results")
    sp.add_argument("query", help="Search query")
    sp.add_argument("--top", type=int, default=5, help="Number of results to collect")

    fp = subparsers.add_parser("fill", help="Fill a form on a webpage")
    fp.add_argument("url", help="Page URL")
    fp.add_argument("--data", required=True, help="JSON file with form data")

    ep = subparsers.add_parser("extract", help="Extract data from a webpage")
    ep.add_argument("url", help="Page URL")
    ep.add_argument("--selector", required=True, help="CSS selector")
    ep.add_argument("--limit", type=int, default=10, help="Max items to extract")

    args = parser.parse_args()
    config = AgentConfig.from_env()
    if args.headless:
        config.browser.headless = True
    asyncio.run(run_command(args, config))


async def run_command(args, config):
    from browser_use import Agent, ChatOpenAI

    llm = ChatOpenAI(
        model=config.llm.model,
        api_key=config.llm.api_key or "fallback-key",
        base_url=config.llm.base_url,
        dont_force_structured_output=True,
    )

    if args.command == "search":
        task = f'Search for "{args.query}" and summarize the top {args.top} results'
        agent = Agent(task=task, llm=llm)
    elif args.command == "fill":
        import json
        with open(args.data, encoding="utf-8") as fh:
            data = json.load(fh)
        fields = ", ".join(f"{k}={v}" for k, v in data.items())
        task = f"Go to {args.url} and fill in the form with: {fields}"
        agent = Agent(task=task, llm=llm)
    elif args.command == "extract":
        task = f'Go to {args.url}, find all elements matching "{args.selector}", extract their text, and return up to {args.limit} results'
        agent = Agent(task=task, llm=llm)
    else:
        print("Unknown command", file=sys.stderr)
        sys.exit(1)

    print(f"Running: {task}")
    result = await agent.run(max_steps=config.llm.max_steps)
    print("\n--- Result ---")
    if hasattr(result, "final_result") and result.final_result:
        print(result.final_result)
    else:
        for item in getattr(result, "all_results", []):
            if hasattr(item, "extracted_content") and item.extracted_content:
                print(item.extracted_content)
    print("--- End ---")


if __name__ == "__main__":
    main()
