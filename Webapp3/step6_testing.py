import streamlit as st
from stable_baselines3 import DQN
from stable_baselines3 import PPO
import gymnasium as gym
import sqlite3
import json

def load_training_configuration(run_id):
    conn = sqlite3.connect("training_history.db")
    c = conn.cursor()

    c.execute('SELECT env_name, env_params, model_name, model_params, model_path FROM training_history WHERE id = ?', (run_id,))
    row = c.fetchone()
    conn.close()

    st.session_state["selected_env"] = row[0]
    st.session_state["env_params"] = json.loads(row[1])
    st.session_state["model"] = row[2]
    st.session_state["model_params"] = json.loads(row[3])
    st.session_state["model_path"] = row[4]
    # if run_id != 1:
    st.success(f"Configuration ID {run_id} loaded successfully!")

def get_last_id():
    conn = sqlite3.connect("training_history.db")
    c = conn.cursor()
    c.execute("SELECT MAX(id) FROM training_history")
    last_id = c.fetchone()[0]
    conn.close()
    return last_id if last_id is not None else 0


# config = {}
# config["initial_spacing"] = 2
# config["vehicles_count"] = 50
# config["lanes_count"] = 4
# config["offscreen_rendering"] = False
# model_path = './models/model_1'

def run():
    config = {}
    st.header("Step 6: Testing")
    maximum_id = get_last_id()
    # load_training_configuration(1)
    configID = st.number_input("Enter the Configuration ID", min_value=1, max_value=maximum_id, value=1, step=1)

    if st.button(f"Load Configuration RUN ID {configID}"):
        load_training_configuration(configID)

    model_path = st.session_state.get("model_path")
    config = st.session_state.get("env_params")
    if config is not None:
        config["offscreen_rendering"] = False
    # print(config["lanes_count"])
    # --- env configure
    selected_env = st.session_state.get("selected_env", "highway-v0")
    Model = st.session_state.get("model", "DQN")
    if selected_env == "highway-v0":
        if config is not None:
            spacing = config["initial_spacing"]
            num_vehicles = config["vehicles_count"]
            num_lanes = config["lanes_count"]
            render = config["offscreen_rendering"]
        # output the configuration
            st.write(f"Environment: {selected_env}")
            st.write(f"Vehicle Spacing: {spacing}")
            st.write(f"Number of Vehicles: {num_vehicles}")
            st.write(f"Number of Lanes: {num_lanes}")
        # st.write(f"Off-screen rendering: {render}")
        st.write(f"model path is", model_path)
        # config = {
        #         "lanes_count": num_lanes,
        #         "vehicles_count": num_vehicles,
        #         "initial_spacing": spacing,
        #     }

    elif selected_env == "roundabout-v0":
        render = st.session_state.get("rendering", False)
        # config = {"offscreen_rendering": render}
    elif selected_env == "intersection-v0":
        render = st.session_state.get("rendering", False)
        # config = {"offscreen_rendering": render}
    else:
        render = st.session_state.get("rendering", False)
        # config = {"offscreen_rendering": render}
    
    env = gym.make(selected_env, config=config)
    env.reset()
    if st.button("Start Testing"):
        if Model == 'DQN':
            model = DQN.load(model_path, env=env)
        if Model == 'PPO':
            model = PPO.load(model_path, env=env)
        # env = RecordVideo(env, video_folder="racetrack_ppo/videos", episode_trigger=lambda e: True)
        # env.unwrapped.set_record_video_wrapper(env)
        env.configure({"simulation_frequency": 15})  # Higher FPS for rendering

        for videos in range(1):
            done = truncated = False
            obs, info = env.reset()
            while not (done or truncated):
                # Predict
                action, _states = model.predict(obs, deterministic=True)
                # Get reward
                obs, reward, done, truncated, info = env.step(action)
                # Render
                env.render()
        env.close()



