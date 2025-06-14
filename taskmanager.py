import streamlit as st
import json
import os
from datetime import date

# 📁 Create tasks directory if not exists
if not os.path.exists("tasks"):
    os.makedirs("tasks")

# 📄 Get file path for selected date
def get_task_file(selected_date):
    return f"tasks/{selected_date}.json"

# 📥 Load tasks (with support for old format)
def load_tasks(selected_date):
    filepath = get_task_file(selected_date)
    try:
        if os.path.exists(filepath):
            with open(filepath, "r") as file:
                data = json.load(file)
                # Auto-convert old string list to dict format
                if data and isinstance(data[0], str):
                    return [{"task": task, "status": "Pending"} for task in data]
                elif isinstance(data[0], dict):
                    return data
    except Exception:
        st.warning("⚠️ Error loading tasks, reset to empty.")
    return []

# 💾 Save tasks to file
def save_tasks(selected_date, tasks):
    filepath = get_task_file(selected_date)
    with open(filepath, "w") as file:
        json.dump(tasks, file)

# 🧾 Set up Streamlit app
st.set_page_config(page_title="Task Manager", layout="wide")
st.title("📋 Daily Task Manager")

# 📅 Date selection
st.sidebar.header("📅 Select Date")
selected_date = st.sidebar.date_input("Choose a date", value=date.today())
selected_date_str = selected_date.strftime("%Y-%m-%d")

# 📥 Load today's tasks
tasks = load_tasks(selected_date_str)
if not isinstance(tasks, list):
    tasks = []

# ➕ Add new task
st.subheader(f"Tasks for {selected_date_str}")
new_task = st.text_input("Add a new task", placeholder="e.g., Complete report")

if st.button("➕ Add Task"):
    if new_task:
        tasks.append({"task": new_task, "status": "Pending"})
        save_tasks(selected_date_str, tasks)
        st.success("Task added!")
        st.rerun()
    else:
        st.warning("Please enter a task.")

# 📋 Display tasks
if tasks:
    st.write("### ✅ Your Tasks:")
    for i, item in enumerate(tasks):
        col1, col2, col3 = st.columns([0.6, 0.3, 0.1])

        with col1:
            st.write(f"📝 {item['task']}")

        with col2:
            status_options = ["Pending", "Completed"]
            selected_status = st.selectbox(
                "Status",
                status_options,
                index=status_options.index(item.get("status", "Pending")),
                key=f"status_{i}"
            )
            if selected_status != item.get("status"):
                tasks[i]["status"] = selected_status
                save_tasks(selected_date_str, tasks)
                st.rerun()

        with col3:
            if st.button("❌", key=f"delete_{i}"):
                tasks.pop(i)
                save_tasks(selected_date_str, tasks)
                st.rerun()
else:
    st.info("No tasks for this day yet.")

# ℹ️ Footer
st.markdown("---")
st.caption("🛠️ Built with Streamlit | Tasks stored per-day in JSON format.")
