import streamlit as st
import os
import gymnasium as gym
from gymnasium.wrappers import RecordVideo
from stable_baselines3 import DQN
import sys
sys.path.append('/home/yzhang94/Documents/Highway_8112/HighwayEnv/highway_env')

import highway_env
from stable_baselines3.common.callbacks import BaseCallback


# add one call back so that we can visualize the training procedure
class RenderCallback(BaseCallback):
    def __init__(self, env, verbose=0):
        super(RenderCallback, self).__init__(verbose)
        self.env = env

    def _on_step(self) -> bool:
        self.env.render()  # Render the environment at each step
        return True

ENVIRONMENTS = ["highway-v0", "merge-v0", "roundabout-v0", "intersection-v0"]

st.title("Highway-Env Reinforcement Learning Interface")


st.header("Step 1: Select Environment")
selected_env = st.selectbox("Choose an environment:", ENVIRONMENTS)

# Input hyperparameters
st.header("Step 2: Configure Hyperparameters")
learning_rate = st.number_input("Learning Rate:", min_value=0.0001, max_value=1.0, value=0.001, step=0.0001)
batch_size = st.number_input("Batch Size:", min_value=1, max_value=1024, value=64, step=1)
episodes = st.number_input("Number of Episodes:", min_value=1, max_value=10000, value=100, step=1)

# Select model path
st.header("Step 3: Choose Model Path")
model_path = st.text_input("Enter or select a model file path:")
if st.button("Browse Model Path"):
    model_path = st.text_input("Model Path:", os.path.abspath(st.file_uploader("Upload Model File")))

# Select log path
st.header("Step 4: Choose Log Path")
log_path = st.text_input("Enter or select a directory for logs:")
if st.button("Browse Log Path"):
    log_path = st.text_input("Log Path:", st.text_area("Enter log directory path:", ""))

# Start training
st.header("Step 5: Start Training")
if st.button("Start Training"):
    st.write(f"🚀 Training started with the following settings:")
    st.write(f"Environment: {selected_env}")
    st.write(f"Learning Rate: {learning_rate}")
    st.write(f"Batch Size: {batch_size}")
    st.write(f"Episodes: {episodes}")
    st.write(f"Model Path: {model_path}")
    st.write(f"Log Path: {log_path}")
    

    TRAIN = True
    env = gym.make(selected_env)
    obs, info = env.reset()
    callback = RenderCallback(env)
    # Create the model
    model = DQN('MlpPolicy', env,
                policy_kwargs=dict(net_arch=[256, 256]),
                learning_rate=5e-4,
                buffer_size=15000,
                learning_starts=200,
                batch_size=32,
                gamma=0.8,
                train_freq=1,
                gradient_steps=1,
                target_update_interval=50,
                verbose=1,
                tensorboard_log="highway_dqn/")

    # Train the model
    if TRAIN:
        model.learn(total_timesteps=int(2e4), callback=callback)
        model.save("highway_dqn/model")
        del model


    # Replace the following with your training function
    # Example: train(selected_env, learning_rate, batch_size, episodes, model_path, log_path)
    st.success("Training initiated. Check logs for progress!")

# Optional: Visualization or monitoring (can be extended)
st.header("Optional: Visualization")
if st.button("Render Environment"):
    st.write(f"Rendering `{selected_env}`... (Not implemented in this demo)")


