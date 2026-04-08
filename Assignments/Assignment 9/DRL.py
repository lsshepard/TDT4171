import gymnasium as gym
from stable_baselines3 import DQN
from stable_baselines3.common.evaluation import evaluate_policy


env = gym.make("FrozenLake-v1", map_name="8x8", is_slippery=True)

model = DQN("MlpPolicy", env, verbose=1, exploration_fraction=0.3)
model.learn(total_timesteps=int(1e6), progress_bar=True)

mean_rewards, _ = evaluate_policy(model, model.get_env(), n_eval_episodes=100)

print(mean_rewards)