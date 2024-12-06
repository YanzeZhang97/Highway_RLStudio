import streamlit as st
import gymnasium as gym
from stable_baselines3 import DQN
from stable_baselines3 import PPO
import os
from utils.callbacks import RenderCallback
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import SubprocVecEnv
import json
import sqlite3
from stable_baselines3.common.logger import configure

def save_training_data(model_path, env_name, env_params, model_name, model_params, training_steps, log_path):
    conn = sqlite3.connect("training_history.db")
    c = conn.cursor()

    env_params_json = json.dumps(env_params)
    model_params_json = json.dumps(model_params)

    c.execute('''
        INSERT INTO training_history (model_path, env_name, env_params, model_name, model_params, training_steps, log_path)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (model_path, env_name, env_params_json, model_name, model_params_json, training_steps, log_path))

    conn.commit()
    conn.close()


def run():
    st.header("Step 5: Start Training")
    selected_env = st.session_state.get("selected_env", "highway-v0")

    learning_rate = st.session_state.get("learning_rate", 0.001)
    batch_size = st.session_state.get("batch_size", 64)
    steps = st.session_state.get("steps", 2e4)
    model_path = st.session_state.get("model_path", "./model")
    log_path = st.session_state.get("log_path", "./logs")
    Model = st.session_state.get("model", "DQN")

    if selected_env == "highway-v0":
        spacing = st.session_state.get("spacing", 2)
        num_vehicles = st.session_state.get("num_vehicles", 50) 
        num_lanes = st.session_state.get("num_lanes", 4) 
        render = st.session_state.get("rendering", False)
        st.write(f"Environment: {selected_env}")
        st.write(f"Vehicle Spacing: {spacing}")
        st.write(f"Number of Vehicles: {num_vehicles}")
        st.write(f"Number of Lanes: {num_lanes}")
        st.write(f"Off-screen rendering: {render}")
        config = {
                "lanes_count": num_lanes,
                "vehicles_count": num_vehicles,
                "initial_spacing": spacing,
                "offscreen_rendering": render
            }

    elif selected_env == "roundabout-v0":
        render = st.session_state.get("rendering", False)
        config = {"offscreen_rendering": render}
    elif selected_env == "intersection-v0":
        render = st.session_state.get("rendering", False)
        config = {"offscreen_rendering": render}
    else:
        render = st.session_state.get("rendering", False)
        config = {"offscreen_rendering": render}
    
    env = gym.make(selected_env, config=config)
    env.reset()
    callback = RenderCallback(env, st.empty(), {"steps": [], "rewards": []})

    if Model == 'DQN':
        gamma = st.session_state.get("gamma", 0.8)
        policy = st.session_state.get("policy", "MLP")
        Net_Achitecture = st.session_state.get("Net_Achitecture", [255,255])
        # print(Net_Achitecture)
        modelpolicy = 'MlpPolicy'

        model = DQN(
            modelpolicy,
            env,
            policy_kwargs=dict(net_arch=Net_Achitecture),
            learning_rate=learning_rate,
            buffer_size=15000,
            learning_starts=200,
            batch_size=batch_size,
            gamma=gamma,
            train_freq=1,
            gradient_steps=1,
            target_update_interval=50,
            verbose=1,
            tensorboard_log=log_path,
        )

    if Model == 'PPO':
        gamma = st.session_state.get("gamma", 0.8)
        n_cpu = 6
        env = make_vec_env("highway-fast-v0", n_envs=n_cpu, vec_env_cls=SubprocVecEnv)
        model = PPO("MlpPolicy",
                    env,
                    policy_kwargs=dict(net_arch=[dict(pi=[256, 256], vf=[256, 256])]),
                    n_steps=batch_size * 12 // n_cpu,
                    batch_size=batch_size,
                    n_epochs=10,
                    learning_rate=learning_rate,
                    gamma=gamma,
                    verbose=2,
                    tensorboard_log=log_path)
    
    if st.button("Start Training"):
        st.write(f"Training started with the following settings:")
        st.write(f"Environment: {selected_env}")
        st.write(f"Learning Rate: {learning_rate}")
        st.write(f"Batch Size: {batch_size}")
        st.write(f"Steps: {steps}")
        st.write(f"Model Path: {model_path}")
        st.write(f"Log Path: {log_path}")

        model.learn(total_timesteps=int(steps), callback=callback)
        model.save(os.path.join(model_path, f"highway_{Model}_model"))
        specific_log_dir = model.logger.dir
        save_training_data(
            model_path=os.path.join(model_path, f"highway_{Model}_model"),
            env_name=selected_env,
            env_params=config,
            model_name=Model,
            model_params={"learning_rate": learning_rate, "batch_size": batch_size, "gamma": gamma},
            training_steps=steps,
            log_path=log_path)
        st.success("Training completed! Check logs for details.")
