import streamlit as st

def run():
    st.header("Step 3: Choose Model Path")
    model_path = st.text_input("Enter or select a model file path:")
    st.session_state["model_path"] = model_path
