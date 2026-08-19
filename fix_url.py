import pathlib

base = pathlib.Path(r"C:\Users\Administrator\Documents\Codex\2026-08-20\au\work")
app_py = base / "app.py"
content = app_py.read_text(encoding="utf-8")

old = 'base_url=os.getenv("AGENT_BASE_URL", "http://127.0.0.1:57321/v1")'
new = 'base_url=os.getenv("AGENT_BASE_URL", "https://api.deepseek.com/v1")'
content = content.replace(old, new)

app_py.write_text(content, encoding="utf-8")
print("Fixed BASE_URL to DeepSeek")
