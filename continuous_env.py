import gym
import numpy as np

class ContinuousPortfolioEnv(gym.Env):
    def __init__(self):
        super(ContinuousPortfolioEnv, self).__init__()

        self.btc_returns = np.random.randn(2000)
        self.sp500_returns = np.random.randn(2000)
        self.current_step = 0
        self.done = False

        # Action = [btc_weight], sp500_weight = 1 - btc
        self.action_space = gym.spaces.Box(low=0.0, high=1.0, shape=(1,), dtype=np.float32)

        # Observation = today's returns
        self.observation_space = gym.spaces.Box(
            low=-np.inf, high=np.inf, shape=(2,), dtype=np.float32
        )

    def reset(self):
        self.current_step = 0
        self.done = False
        return self._get_observation()

    def step(self, action):
        btc_weight = action[0]
        sp500_weight = 1.0 - btc_weight

        btc_return = self.btc_returns[self.current_step]
        sp_return = self.sp500_returns[self.current_step]

        portfolio_return = btc_weight * btc_return + sp500_weight * sp_return

        self.current_step += 1
        if self.current_step >= len(self.btc_returns):
            self.done = True
            obs = self._get_observation(self.current_step - 1)
        else:
            obs = self._get_observation()

        return obs, portfolio_return, self.done, {}

    def _get_observation(self, step=None):
        step = self.current_step if step is None else step
        return np.array([
            self.btc_returns[step],
            self.sp500_returns[step]
        ], dtype=np.float32)
