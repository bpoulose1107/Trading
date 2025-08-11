import os
import pandas as pd
from stable_baselines3 import DQN
from multi_asset_env import MultiAssetTradingEnv
from discrete_env import DiscreteWrapper

# Create folders
os.makedirs("models", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Load wrapped env
env = DiscreteWrapper(MultiAssetTradingEnv())

# Train DQN
model = DQN("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)

# Save model
model.save("models/dqn_trading_agent")
print("✅ DQN model saved as models/dqn_trading_agent.zip")

# Create dummy log
log = {
    "Step": list(range(1000)),
    "Reward": [0.01] * 1000,
    "BTC_action": [0, 1, 2] * 333 + [0],
    "SP500_action": [2, 1, 0] * 333 + [2],
}
df = pd.DataFrame(log)
df.to_csv("logs/dqn_log.csv", index=False)
print("📄 Dummy DQN log saved as logs/dqn_log.csv")
