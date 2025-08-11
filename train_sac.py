import os
import pandas as pd
import numpy as np
from stable_baselines3 import SAC
from continuous_env import ContinuousPortfolioEnv

os.makedirs("models", exist_ok=True)
os.makedirs("logs", exist_ok=True)

env = ContinuousPortfolioEnv()
model = SAC("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)
model.save("models/sac_trading_agent")
print("✅ SAC model saved as models/sac_trading_agent.zip")

# Dummy log data for testing
log = {
    "Step": list(range(1000)),
    "Reward": np.random.normal(0.01, 0.005, 1000),
    "BTC_action": np.random.choice([0, 1, 2], 1000),
    "SP500_action": np.random.choice([0, 1, 2], 1000),
}
df = pd.DataFrame(log)
df.to_csv("logs/sac_log.csv", index=False)
print("📄 Dummy SAC log saved as logs/sac_log.csv")
