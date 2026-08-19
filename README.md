# Browser Agent

AI-powered browser automation agent built on [browser-use](https://github.com/browser-use/browser-use).

Run web tasks with natural language — search, fill forms, extract data — all driven by an AI agent that controls a real browser.

## Quick Start

### Install

\`\`\`bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
pip install -e ".[dev]"
\`\`\`

### Environment Variables

\`\`\`bash
export AGENT_API_KEY="your-key-here"
export AGENT_BASE_URL="http://127.0.0.1:57321/v1"
export AGENT_MODEL="agnes-2.5-pro"
\`\`\`

Or create a \`.env\` file:
\`\`\`
AGENT_API_KEY=your-key-here
AGENT_BASE_URL=http://127.0.0.1:57321/v1
AGENT_MODEL=agnes-2.5-pro
\`\`\`

### Usage

**Search the web**
\`\`\`bash
python -m browser_agent search "browser automation python"
python -m browser_agent search "latest AI news" --top 10
\`\`\`

**Fill a form**
\`\`\`bash
python -m browser_agent fill "https://example.com/form" --data data.json
\`\`\`

**Extract data**
\`\`\`bash
python -m browser_agent extract "https://example.com/list" --selector ".item" --limit 20
\`\`\`

**Headed mode (watch the browser)**
\`\`\`bash
AGENT_HEADLESS=false python -m browser_agent search "test"
\`\`\`

## Examples

\`\`\`bash
python examples/search.py "your query here"
python examples/fill_form.py "https://example.com/form" examples/data/sample_form.json
python examples/extract.py "https://example.com" ".product-name" --limit 5
\`\`\`

## Configuration

Edit \`configs/default.yaml\` or set environment variables:

| Variable | Default | Description |
|---|---|---|
| AGENT_MODEL | agnes-2.5-pro | LLM model to use |
| AGENT_API_KEY | "" | API key |
| AGENT_BASE_URL | http://127.0.0.1:57321/v1 | LLM API endpoint |
| AGENT_MAX_STEPS | 20 | Max steps per task |
| AGENT_HEADLESS | true | Run browser headless |

## Project Structure

\`\`\`
.
├── browser_agent/
│   ├── __init__.py
│   ├── __main__.py       # CLI entry point
│   └── config.py         # Configuration
├── examples/
│   ├── search.py
│   ├── fill_form.py
│   ├── extract.py
│   └── data/
│       └── sample_form.json
├── configs/
│   └── default.yaml
├── pyproject.toml
├── README.md
└── .gitignore
\`\`\`

## Requirements

- Python 3.10+
- A Chromium-based browser installed on your system
- An OpenAI-compatible LLM API endpoint

## License

MIT
