import streamlit as st
MODELS = ['DQN','PPO']
# DQNPolicy = ['MLP', 'CNN']

def run():
    st.header("Step 2: Configure Model Hyperparameters")
    learning_rate = st.number_input(
        "Learning Rate:",
        min_value=0.0001, max_value=1.0, value=0.001, step=0.0001, format="%.4f"
    )
    batch_size = st.number_input(
        "Batch Size:", min_value=1, max_value=1024, value=64, step=1
    )
    steps = st.number_input(
        "Number of Steps:", min_value=1, max_value=int(2e6), value=int(2e4), step=1
    )
    model = st.selectbox("Choose a model", MODELS)

    st.session_state["learning_rate"] = learning_rate
    st.session_state["batch_size"] = batch_size
    st.session_state["steps"] = steps
    st.session_state["model"] = model

    if model == 'DQN':
        Net_Achitecture = st.text_input("Enter a list of numbers (e.g., [255, 255]):")
        # Net_Achitecture = st.text_input()
        if Net_Achitecture:
            user_list = eval(Net_Achitecture)  
            if isinstance(user_list, list) and all(isinstance(i, (int, float)) for i in user_list):
                st.success(f"Valid list entered: {user_list}")
                st.session_state["Net_Achitecture"] = user_list
            else:
                st.error("Please enter a valid list of numbers.")

        # st.session_state["Net_Achitecture"] = Net_Achitecture
        # print(isinstance(Net_Achitecture, list))
        gamma = st.number_input("gamma:", 
                                min_value=0.01, max_value=1.0, value=0.8, 
                                step=0.01, format="%.2f")
        st.session_state["gamma"] = gamma
        # policy = st.selectbox("select a traning policy", DQNPolicy)
        # st.session_state["policy"] = policy

    if model == 'PPO':
        Net_Achitecture = st.text_input("Enter a list of numbers (e.g., [255, 255]):")
        # Net_Achitecture = st.text_input()
        if Net_Achitecture:
            # Convert the string input into a Python list
            user_list = eval(Net_Achitecture) 
            if isinstance(user_list, list) and all(isinstance(i, (int, float)) for i in user_list):
                st.success(f"Valid list entered: {user_list}")
                st.session_state["Net_Achitecture"] = user_list
            else:
                st.error("Please enter a valid list of numbers.")

        # st.session_state["Net_Achitecture"] = Net_Achitecture
        # print(isinstance(Net_Achitecture, list))
        gamma = st.number_input("gamma:", 
                                min_value=0.01, max_value=1.0, value=0.8, 
                                step=0.01, format="%.2f")
        st.session_state["gamma"] = gamma
        # policy = st.selectbox("select a traning policy", DQNPolicy)
        # st.session_state["policy"] = policy


    st.write("### Model Configuration")
    st.write(f"learning_rate: {learning_rate}")
    st.write(f"batch_size: {batch_size}")
    st.write(f"training steps: {steps}")
    st.write(f"selected model is: {model}")
