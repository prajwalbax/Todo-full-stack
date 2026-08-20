import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Task Manager",
    page_icon="✅",
    layout="centered"
)

# -------------------------
# API Helper Functions
# -------------------------

def fetch_tasks():
    try:
        response = requests.get(f"{API_URL}/tasks", timeout=5)
        if response.status_code == 200:
            return response.json()
        st.error("Failed to fetch tasks from server.")
    except requests.exceptions.RequestException as e:
        st.error(f"Server connection error: {e}")
    return []

def add_task(title: str):
    try:
        res = requests.post(f"{API_URL}/tasks", json={"title": title}, timeout=5)
        return res.status_code == 200
    except requests.exceptions.RequestException:
        return False

def toggle_task(task_id: int, completed: bool):
    try:
        res = requests.put(
            f"{API_URL}/tasks/{task_id}", 
            json={"completed": completed}, 
            timeout=5
        )
        return res.status_code == 200
    except requests.exceptions.RequestException:
        return False

def remove_task(task_id: int):
    try:
        res = requests.delete(f"{API_URL}/tasks/{task_id}", timeout=5)
        return res.status_code == 200
    except requests.exceptions.RequestException:
        return False


# -------------------------
# UI Layout
# -------------------------

st.title("✅ Task Manager")

tasks = fetch_tasks()

# Metrics Summary
total_tasks = len(tasks)
completed_tasks = sum(1 for t in tasks if t.get("completed", False))
pending_tasks = total_tasks - completed_tasks

m1, m2, m3 = st.columns(3)
m1.metric("Total", total_tasks)
m2.metric("Pending", pending_tasks)
m3.metric("Completed", completed_tasks)

st.divider()

# Add Task Form
with st.form("task_form", clear_on_submit=True):
    col_input, col_btn = st.columns([4, 1])
    
    with col_input:
        title = st.text_input(
            "Task Title", 
            placeholder="What needs to be done?", 
            label_visibility="collapsed"
        )
    with col_btn:
        submitted = st.form_submit_button("Add Task", use_container_width=True)

    if submitted:
        if not title.strip():
            st.warning("Please enter a task description.")
        else:
            if add_task(title.strip()):
                st.toast("Task added!", icon="🎉")
                st.rerun()
            else:
                st.error("Failed to add task.")

st.divider()

# Task List View
st.subheader("Tasks")

if not tasks:
    st.info("No tasks yet. Add one above!")
else:
    for task in tasks:
        task_id = task.get("id")
        task_title = task.get("title", "")
        is_completed = task.get("completed", False)

        with st.container(border=True):
            c1, c2, c3 = st.columns([0.1, 0.8, 0.1])

            with c1:
                checked = st.checkbox(
                    "Complete",
                    value=is_completed,
                    key=f"check_{task_id}",
                    label_visibility="collapsed"
                )
                if checked != is_completed:
                    if toggle_task(task_id, checked):
                        st.rerun()

            with c2:
                if is_completed:
                    st.markdown(f"~~{task_title}~~")
                else:
                    st.markdown(f"**{task_title}**")

            with c3:
                if st.button("🗑️", key=f"delete_{task_id}", help="Delete Task"):
                    if remove_task(task_id):
                        st.toast("Task deleted", icon="🗑️")
                        st.rerun()
                    else:
                        st.error("Delete failed")