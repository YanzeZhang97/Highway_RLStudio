import matplotlib.pyplot as plt
from stable_baselines3.common.callbacks import BaseCallback

class RenderCallback(BaseCallback):
    def __init__(self, env, progress_placeholder, plot_data, verbose=0):
        super(RenderCallback, self).__init__(verbose)
        self.env = env
        self.progress_placeholder = progress_placeholder
        self.plot_data = plot_data
        self.episode_rewards = []
        self.episode_lengths = []

    def _on_step(self) -> bool:
        # Render the environment
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
