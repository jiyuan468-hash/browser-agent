"""AI Browser Agent - Streamlit Web UI"""
import asyncio
import json
import os
import threading
import uuid
import queue
import streamlit as st
from browser_use import Agent, ChatOpenAI

st.set_page_config(page_title="Browser Agent", page_icon="?", layout="wide")

st.title("Browser Agent")
st.markdown("AI-powered browser automation. Search, fill forms, or extract data from any website.")
st.markdown("[Browser Use](https://github.com/MagMueller/browser-use) -- Built on MagMueller's open-source library.")
st.markdown("---")

with st.sidebar:
    st.header("Configuration")
    st.session_state.model = st.selectbox("LLM Model", ["agnes-2.5-pro", "agnes-2.5-flash", "agnes-2.0-flash"], index=0)
    st.session_state.max_steps = st.slider("Max Steps", 5, 100, 20)
    st.session_state.headless = st.checkbox("Headless Mode", value=True)
    st.markdown("*Uses OpenAI-compatible API (set AGENT_BASE_URL env var)*")

def get_llm():
    return ChatOpenAI(
        model=st.session_state.model,
        api_key=os.getenv("AGENT_API_KEY", "fallback-key"),
        base_url=os.getenv("AGENT_BASE_URL", "http://127.0.0.1:57321/v1"),
        dont_force_structured_output=True
    )

def format_result(result):
    if hasattr(result, "final_result") and result.final_result:
        return f"**Result:**\n\n{result.final_result}"
    output = ""
    for item in getattr(result, "all_results", []):
        if hasattr(item, "extracted_content") and item.extracted_content:
            output += item.extracted_content + "\n"
    return output if output else "**Task completed.**"

async def run_agent(task, q):
    try:
        llm = get_llm()
        agent = Agent(task=task, llm=llm)
        result = await agent.run(max_steps=st.session_state.max_steps)
        q.put(("done", result))
    except Exception as e:
        q.put(("error", e))

def start_task(task, task_id):
    q = queue.Queue()
    st.session_state[task_id + "_q"] = q
    t = threading.Thread(target=run_agent, args=(task, q), daemon=True)
    t.start()
    st.session_state[task_id + "_running"] = True

def check_task(task_id):
    q_key = task_id + "_q"
    running_key = task_id + "_running"
    if not st.session_state.get(running_key, False):
        return None
    q = st.session_state.get(q_key)
    if q is None:
        return None
    try:
        status, value = q.get(timeout=0.01)
        st.session_state[task_id] = value
        st.session_state[running_key] = False
        if status == "error":
            return ("error", value)
        return ("done", value)
    except queue.Empty:
        return None

tab1, tab2, tab3 = st.tabs(["Search", "Fill Form", "Extract"])

with tab1:
    st.subheader("Web Search")
    query = st.text_input("What to search?", placeholder="e.g. browser automation Python")
    top_n = st.slider("Top results", 1, 20, 5)
    if st.button("Run Search", type="primary"):
        tid = str(uuid.uuid4())
        st.session_state[tid] = None
        st.session_state[tid + "_running"] = False
        start_task(f'Search for "{query}" and summarize the top {top_n} results', tid)
    r = check_task(tid)
    if r is None and st.session_state.get(tid + "_running", False):
        st.spinner("Searching the web...")
    elif r is not None:
        if r[0] == "error":
            st.error(f"Error: {r[1]}")
            st.session_state[tid + "_running"] = False
        else:
            st.success("Done!")
            st.markdown(format_result(r[1]))

with tab2:
    st.subheader("Fill a Form")
    form_url = st.text_input("Form URL", placeholder="https://example.com/form")
    json_data = st.text_area("Form data (JSON)", placeholder='{"name": "John", "email": "john@example.com"}')
    if st.button("Fill Form", type="primary"):
        try:
            data = json.loads(json_data)
        except Exception as e:
            st.error(f"Invalid JSON: {e}")
            data = None
        if not form_url or not data:
            st.error("Please provide URL and valid JSON data")
        else:
            tid = str(uuid.uuid4())
            st.session_state[tid] = None
            st.session_state[tid + "_running"] = False
            fields = ", ".join(f"{k}={v}" for k, v in data.items())
            start_task(f"Go to {form_url} and fill in the form with: {fields}", tid)
    r = check_task(tid)
    if r is None and st.session_state.get(tid + "_running", False):
        st.spinner("Filling the form...")
    elif r is not None:
        if r[0] == "error":
            st.error(f"Error: {r[1]}")
            st.session_state[tid + "_running"] = False
        else:
            st.success("Done!")
            st.markdown(format_result(r[1]))

with tab3:
    st.subheader("Extract Data")
    extract_url = st.text_input("Page URL", placeholder="https://example.com/list")
    selector = st.text_input("CSS Selector", placeholder=".item-title")
    limit = st.slider("Max items", 1, 50, 10)
    if st.button("Extract", type="primary"):
        if not extract_url or not selector:
            st.error("Please provide URL and CSS selector")
        else:
            tid = str(uuid.uuid4())
            st.session_state[tid] = None
            st.session_state[tid + "_running"] = False
            start_task(f'Go to {extract_url}, find all elements matching "{selector}", extract their text, and return up to {limit} results', tid)
    r = check_task(tid)
    if r is None and st.session_state.get(tid + "_running", False):
        st.spinner("Extracting data...")
    elif r is not None:
        if r[0] == "error":
            st.error(f"Error: {r[1]}")
            st.session_state[tid + "_running"] = False
        else:
            st.success("Done!")
            st.markdown(format_result(r[1]))
