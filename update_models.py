import pathlib

base = pathlib.Path(r"C:\Users\Administrator\Documents\Codex\2026-08-20\au\work")
app_py = base / "app.py"
content = app_py.read_text(encoding="utf-8")

# Update model dropdown - use DeepSeek models
old = 'st.session_state.model = st.selectbox("LLM Model", ["agnes-2.5-pro", "agnes-2.5-flash", "agnes-2.0-flash"], index=0)'
new = 'st.session_state.model = st.selectbox("LLM Model", ["deepseek-chat", "deepseek-coder", "deepseek-v3"], index=0)'
content = content.replace(old, new)

# Update hint text
content = content.replace("*Uses OpenAI-compatible API (set AGENT_BASE_URL env var)*", "*Uses DeepSeek API (set AGENT_API_KEY env var)*")

# Update the sidebar tip in README
content = content.replace('AGENT_MODEL = "agnes-2.5-pro"', 'AGENT_MODEL = "deepseek-chat"')

app_py.write_text(content, encoding="utf-8")
print("app.py updated, size:", len(content))
