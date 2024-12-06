import streamlit as st

def run():
    st.header("Step 4: Choose Log Path")
    log_path = st.text_input("Enter or select a directory for logs:")
    st.session_state["log_path"] = log_path
