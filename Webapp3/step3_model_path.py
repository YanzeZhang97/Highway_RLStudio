import streamlit as st
import sqlite3

def get_last_id():
    conn = sqlite3.connect("training_history.db")
    c = conn.cursor()
    c.execute("SELECT MAX(id) FROM training_history")
    last_id = c.fetchone()[0]
    conn.close()
    return last_id if last_id is not None else 0  # Return 0 if no rows exist


def run():
    st.header("Step 3: Choose Model Path")
    last_id = get_last_id() + 1
    default_path = f"./models/model_{last_id}"
    model_path = st.text_input("Enter or select a model file path:", value=default_path)
    st.session_state["model_path"] = model_path
