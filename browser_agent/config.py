"""Configuration loader for BrowserAgent."""
import os
from dataclasses import dataclass, field


@dataclass
class LLMConfig:
    model: str = "agnes-2.5-pro"
    api_key: str = ""
    base_url: str = "http://127.0.0.1:57321/v1"
    max_steps: int = 20


@dataclass
class BrowserConfig:
    headless: bool = True
    wait_time: float = 1.0
    screenshot_on_error: bool = True
    output_dir: str = "output"


@dataclass
class AgentConfig:
    llm: LLMConfig = field(default_factory=LLMConfig)
    browser: BrowserConfig = field(default_factory=BrowserConfig)

    @classmethod
    def from_env(cls):
        llm = LLMConfig(
            model=os.getenv("AGENT_MODEL", "agnes-2.5-pro"),
            api_key=os.getenv("AGENT_API_KEY", ""),
            base_url=os.getenv("AGENT_BASE_URL", "http://127.0.0.1:57321/v1"),
            max_steps=int(os.getenv("AGENT_MAX_STEPS", "20")),
        )
        browser = BrowserConfig(
            headless=os.getenv("AGENT_HEADLESS", "true").lower() == "true",
        )
        return cls(llm=llm, browser=browser)
