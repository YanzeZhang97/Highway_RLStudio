import streamlit as st

def run():
    st.header("Step 2: Configure Hyperparameters")
    learning_rate = st.number_input(
        "Learning Rate:",
        min_value=0.0001, max_value=1.0, value=0.001, step=0.0001, format="%.4f"
    )
    batch_size = st.number_input(
        "Batch Size:", min_value=1, max_value=1024, value=64, step=1
    )
    episodes = st.number_input(
        "Number of Episodes:", min_value=1, max_value=10000, value=100, step=1
    )

    st.session_state["learning_rate"] = learning_rate
    st.session_state["batch_size"] = batch_size
    st.session_state["episodes"] = episodes
