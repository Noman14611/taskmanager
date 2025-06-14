import streamlit as st
import json
import os
from datetime import date

# Create directory to store tasks if not exists
if not os.path.exists("tasks"):
    os.makedirs("tasks")

def get_task_file(selected_date):
    return f"tasks/{selected_date}.json"

def load_tasks(selected_date):
    filepath = get_task_file(selected_date)
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            return json.load(file)
    return []

def save_tasks(selected_date, tasks):
    filepath = get_task_file(selected_date)
    with open(filepath, "w") as file:
        json.dump(tasks, file)

# Streamlit app
st.set_page_config(page_title="Task Manager", layout="wide")
st.title("📋 Daily Task Manager")

# Sidebar for date selection
st.sidebar.header("📅 Select Date")
selected_date = st.sidebar.date_input("Choose a date", value=date.today())
selected_date_str = selected_date.strftime("%Y-%m-%d")

# Load tasks for selected date
tasks = load_tasks(selected_date_str)

# Input new task
st.subheader(f"Tasks for {selected_date_str}")
new_task = st.text_input("Add a new task", placeholder="e.g., Complete report")

if st.button("➕ Add Task"):
    if new_task:
        tasks.append(new_task)
        save_tasks(selected_date_str, tasks)
        st.success("Task added!")
        st.experimental_rerun()
    else:
        st.warning("Please enter a task.")

# Display task list
if tasks:
    st.write("### ✅ Your Tasks:")
    for i, task in enumerate(tasks):
        col1, col2 = st.columns([0.9, 0.1])
        with col1:
            st.write(f"📝 {task}")
        with col2:
            if st.button("❌", key=f"delete_{i}"):
                tasks.pop(i)
                save_tasks(selected_date_str, tasks)
                st.experimental_rerun()
else:
    st.info("No tasks for this day yet.")

# Footer
st.markdown("---")
st.caption("🛠️ Built with Streamlit | Task saved in local JSON files.")
