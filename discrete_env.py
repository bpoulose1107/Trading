import gym
import numpy as np

class DiscreteWrapper(gym.Wrapper):
    def __init__(self, env):
        super(DiscreteWrapper, self).__init__(env)

        # Convert MultiDiscrete([3, 3]) → Discrete(9)
        self.action_space = gym.spaces.Discrete(9)

        # Store reverse mapping for later
        self._multi_action_shape = [3, 3]
        self._all_actions = [
            [i, j] for i in range(3) for j in range(3)
        ]

    def reset(self):
        return self.env.reset()

    def step(self, action):
        # Convert 0–8 → [btc_action, sp500_action]
        multi_action = self._all_actions[action]
        return self.env.step(multi_action)
