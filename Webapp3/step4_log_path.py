import streamlit as st
import sqlite3

def get_last_id():
    conn = sqlite3.connect("training_history.db")
    c = conn.cursor()
    c.execute("SELECT MAX(id) FROM training_history")
    last_id = c.fetchone()[0]
    conn.close()
    return last_id if last_id is not None else 0

def run():
    st.header("Step 4: Choose Log Path")
    last_id = get_last_id() + 1
    default_path = f"./logs/log_{last_id}"
    log_path = st.text_input("Enter or select a directory for logs:", value=default_path)
    st.session_state["log_path"] = log_path
