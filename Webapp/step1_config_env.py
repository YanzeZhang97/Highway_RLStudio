import streamlit as st

def run():
    st.header("Step 1: Configure Environment")
    ENVIRONMENTS = ["highway-v0", "merge-v0", "roundabout-v0", "intersection-v0"]
    selected_env = st.selectbox("Choose an environment:", ENVIRONMENTS)
    st.session_state["selected_env"] = selected_env
    
