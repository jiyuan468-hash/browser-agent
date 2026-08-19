import pathlib

base = pathlib.Path(r"C:\Users\Administrator\Documents\Codex\2026-08-20\au\work")
app_py = base / "app.py"
content = app_py.read_text(encoding="utf-8")

old_section = '''tab1, tab2, tab3 = st.tabs(["Search", "Fill Form", "Extract"])

with tab1:
    st.subheader("Web Search")
    query = st.text_input("What to search?", placeholder="e.g. browser automation Python")
    top_n = st.slider("Top results", 1, 20, 5)
    if st.button("Run Search", type="primary"):
        tid = str(uuid.uuid4())
        st.session_state[tid] = None
        st.session_state[tid + "_running"] = False
        start_task(f\'Search for "{query}" and summarize the top {top_n} results\', tid)
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
    json_data = st.text_area("Form data (JSON)", placeholder=\'{"name": "John", "email": "john@example.com"}\')
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
            start_task(f\'Go to {extract_url}, find all elements matching "{selector}", extract their text, and return up to {limit} results\', tid)
    r = check_task(tid)
    if r is None and st.session_state.get(tid + "_running", False):
        st.spinner("Extracting data...")
    elif r is not None:
        if r[0] == "error":
            st.error(f"Error: {r[1]}")
            st.session_state[tid + "_running"] = False
        else:
            st.success("Done!")
            st.markdown(format_result(r[1]))'''

new_section = '''tab1, tab2, tab3 = st.tabs(["Search", "Fill Form", "Extract"])

with tab1:
    st.subheader("Web Search")
    query = st.text_input("What to search?", placeholder="e.g. browser automation Python")
    top_n = st.slider("Top results", 1, 20, 5)
    if "search_tid" not in st.session_state:
        st.session_state["search_tid"] = None
    if st.button("Run Search", type="primary"):
        st.session_state["search_tid"] = str(uuid.uuid4())
        st.session_state[st.session_state["search_tid"]] = None
        st.session_state[st.session_state["search_tid"] + "_running"] = False
        start_task(f\'Search for "{query}" and summarize the top {top_n} results\', st.session_state["search_tid"])
    tid = st.session_state["search_tid"]
    if tid:
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
    json_data = st.text_area("Form data (JSON)", placeholder=\'{"name": "John", "email": "john@example.com"}\')
    if "fill_tid" not in st.session_state:
        st.session_state["fill_tid"] = None
    if st.button("Fill Form", type="primary"):
        try:
            data = json.loads(json_data)
        except Exception as e:
            st.error(f"Invalid JSON: {e}")
            data = None
        if not form_url or not data:
            st.error("Please provide URL and valid JSON data")
        else:
            st.session_state["fill_tid"] = str(uuid.uuid4())
            st.session_state[st.session_state["fill_tid"]] = None
            st.session_state[st.session_state["fill_tid"] + "_running"] = False
            fields = ", ".join(f"{k}={v}" for k, v in data.items())
            start_task(f"Go to {form_url} and fill in the form with: {fields}", st.session_state["fill_tid"])
    tid = st.session_state["fill_tid"]
    if tid:
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
    if "extract_tid" not in st.session_state:
        st.session_state["extract_tid"] = None
    if st.button("Extract", type="primary"):
        if not extract_url or not selector:
            st.error("Please provide URL and CSS selector")
        else:
            st.session_state["extract_tid"] = str(uuid.uuid4())
            st.session_state[st.session_state["extract_tid"]] = None
            st.session_state[st.session_state["extract_tid"] + "_running"] = False
            start_task(f\'Go to {extract_url}, find all elements matching "{selector}", extract their text, and return up to {limit} results\', st.session_state["extract_tid"])
    tid = st.session_state["extract_tid"]
    if tid:
        r = check_task(tid)
        if r is None and st.session_state.get(tid + "_running", False):
            st.spinner("Extracting data...")
        elif r is not None:
            if r[0] == "error":
                st.error(f"Error: {r[1]}")
                st.session_state[tid + "_running"] = False
            else:
                st.success("Done!")
                st.markdown(format_result(r[1]))'''

if old_section in content:
    content = content.replace(old_section, new_section)
    app_py.write_text(content, encoding="utf-8")
    print("app.py fixed successfully")
else:
    print("Could not find the target section, trying alternative approach")
    print("Content length:", len(content))
    # Find the tab1 section
    if 'with tab1:' in content:
        print("Found tab1 section")
    if 'r = check_task(tid)' in content:
        print("Found check_task calls")
