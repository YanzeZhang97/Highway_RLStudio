import streamlit as st
import gymnasium as gym
from stable_baselines3 import DQN
import os
from utils.callbacks import RenderCallback

def run():
    st.header("Step 5: Start Training")
    if st.button("Start Training"):
        selected_env = st.session_state.get("selected_env", "highway-v0")
        learning_rate = st.session_state.get("learning_rate", 0.001)
        batch_size = st.session_state.get("batch_size", 64)
        episodes = st.session_state.get("episodes", 100)
        model_path = st.session_state.get("model_path", "./model")
        log_path = st.session_state.get("log_path", "./logs")

        st.write(f"🚀 Training started with the following settings:")
        st.write(f"Environment: {selected_env}")
        st.write(f"Learning Rate: {learning_rate}")
        st.write(f"Batch Size: {batch_size}")
        st.write(f"Episodes: {episodes}")
        st.write(f"Model Path: {model_path}")
        st.write(f"Log Path: {log_path}")

        env = gym.make(selected_env, config = {})
        env.reset()

        callback = RenderCallback(env, st.empty(), {"steps": [], "rewards": []})

        model = DQN(
            'MlpPolicy',
            env,
            policy_kwargs=dict(net_arch=[256, 256]),
            learning_rate=learning_rate,
            buffer_size=15000,
            learning_starts=200,
            batch_size=batch_size,
            gamma=0.8,
            train_freq=1,
            gradient_steps=1,
            target_update_interval=50,
            verbose=1,
            tensorboard_log=log_path,
        )

        model.learn(total_timesteps=int(episodes * 200), callback=callback)
        model.save(os.path.join(model_path, "highway_dqn_model"))

        st.success("Training completed! Check logs for details.")
