import gym
import numpy as np

class MultiAssetTradingEnv(gym.Env):
    def __init__(self):
        super(MultiAssetTradingEnv, self).__init__()
        
        # Simulated 2000-day price data
        self.btc_prices = np.random.randn(2000)
        self.sp500_prices = np.random.randn(2000)

        self.current_step = 0
        self.done = False

        # Action space: [Buy, Hold, Sell] for each asset (3x3 = 9 combinations)
        self.action_space = gym.spaces.MultiDiscrete([3, 3])

        # Observation: [btc_price_today, sp500_price_today]
        self.observation_space = gym.spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(2,),
            dtype=np.float32
        )

    def reset(self):
        self.current_step = 0
        self.done = False
        return self._get_observation()

    def step(self, action):
        btc_action, sp_action = action

        btc_return = self.btc_prices[self.current_step]
        sp_return = self.sp500_prices[self.current_step]

        reward = 0
        if btc_action == 0:  # Buy
            reward += btc_return
        if sp_action == 0:  # Buy
            reward += sp_return

        self.current_step += 1
        if self.current_step >= len(self.btc_prices):
            self.done = True
            obs = self._get_observation(self.current_step - 1)  # stay in range
        else:
            obs = self._get_observation()

        return obs, reward, self.done, {}

    def _get_observation(self, step=None):
        step = self.current_step if step is None else step
        return np.array([
            self.btc_prices[step],
            self.sp500_prices[step]
        ], dtype=np.float32)
