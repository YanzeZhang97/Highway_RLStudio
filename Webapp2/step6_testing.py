import streamlit as st
from stable_baselines3 import DQN
from stable_baselines3 import PPO
import gymnasium as gym


def run():
    st.header("Step 6: Testing")
    model_path = st.text_input("Enter or select a model file path:")
    st.session_state["model_path"] = model_path

    # --- env configure
    selected_env = st.session_state.get("selected_env", "highway-v0")
    Model = st.session_state.get("model", "DQN")
    if selected_env == "highway-v0":
        spacing = st.session_state.get("spacing", 2)
        num_vehicles = st.session_state.get("num_vehicles", 50) 
        num_lanes = st.session_state.get("num_lanes", 4) 
        render = st.session_state.get("rendering", False)
        # output the configuration
        st.write(f"Environment: {selected_env}")
        st.write(f"Vehicle Spacing: {spacing}")
        st.write(f"Number of Vehicles: {num_vehicles}")
        st.write(f"Number of Lanes: {num_lanes}")
        st.write(f"Off-screen rendering: {render}")
        config = {
                "lanes_count": num_lanes,
                "vehicles_count": num_vehicles,
                "initial_spacing": spacing,
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
    if st.button("Start Testing"):
        if Model == 'DQN':
            model = DQN.load(model_path, env=env)
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



