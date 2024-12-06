import streamlit as st
import os
import gymnasium as gym
from gymnasium.wrappers import RecordVideo
from stable_baselines3 import DQN
import matplotlib.pyplot as plt
import time
import sys

sys.path.append('/home/yzhang94/Documents/Highway_8112/HighwayEnv/highway_env')
import highway_env
from stable_baselines3.common.callbacks import BaseCallback

# Custom callback for training visualization
class RenderCallback(BaseCallback):
    def __init__(self, env, progress_placeholder, plot_data, verbose=0):
        super(RenderCallback, self).__init__(verbose)
        self.env = env
        self.progress_placeholder = progress_placeholder
        self.plot_data = plot_data
        self.episode_rewards = []
        self.episode_lengths = []
        self.total_steps = 0

    def _on_step(self) -> bool:
        self.env.render()

        # Update reward visualization
        if self.locals.get("infos"):
            for info in self.locals["infos"]:
                if "episode" in info.keys():
                    self.episode_rewards.append(info["episode"]["r"])
                    self.episode_lengths.append(info["episode"]["l"])
                    self.update_plot()

        return True

    def update_plot(self):
        # Update the Streamlit placeholder with a new plot
        self.plot_data["rewards"] = self.episode_rewards[-100:]  # Last 100 rewards
        self.plot_data["steps"] = list(range(len(self.plot_data["rewards"])))

        fig, ax = plt.subplots()
        ax.plot(self.plot_data["steps"], self.plot_data["rewards"], label="Rewards")
        ax.set_title("Training Progress")
        ax.set_xlabel("Episode")
        ax.set_ylabel("Reward")
        ax.legend()
        self.progress_placeholder.pyplot(fig)
        plt.close(fig)


ENVIRONMENTS = ["highway-v0", "merge-v0", "roundabout-v0", "intersection-v0"]

st.title("Train Your Highway Agent")
st.header("Step 1: Config Env")
selected_env = st.selectbox("Choose an environment:", ENVIRONMENTS)


st.header("Step 2: Configure Hyperparameters")
learning_rate = st.number_input("Learning Rate:", min_value=0.0001, max_value=1.0, value=0.001, step=0.0001, format="%.6f")
batch_size = st.number_input("Batch Size:", min_value=1, max_value=1024, value=64, step=1)
episodes = st.number_input("Number of Episodes:", min_value=1, max_value=10000, value=100, step=1)


st.header("Step 3: Choose Model Path")
model_path = st.text_input("Enter or select a model file path:")


st.header("Step 4: Choose Log Path")
log_path = st.text_input("Enter or select a directory for logs:")


progress_placeholder = st.empty()
plot_data = {"steps": [], "rewards": []}


env = gym.make(selected_env)
env.reset()


callback = RenderCallback(env, progress_placeholder, plot_data)


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



st.header("Step 5: Start Training")
if st.button("Start Training"):
    st.write(f"🚀 Training started with the following settings:")
    st.write(f"Environment: {selected_env}")
    st.write(f"Learning Rate: {learning_rate}")
    st.write(f"Batch Size: {batch_size}")
    st.write(f"Episodes: {episodes}")
    st.write(f"Model Path: {model_path}")
    st.write(f"Log Path: {log_path}")


    # Train the model
    model.learn(total_timesteps=int(episodes * 200), callback=callback)
    model.save(os.path.join(model_path, "highway_dqn_model"))
    del model

    st.success("Training completed! Check logs for details.")

# Optional: Visualization or monitoring
st.header("Optional: Visualization")
if st.button("Render Environment"):
    st.write(f"Rendering `{selected_env}`... (Not implemented in this demo)")
