__author__ = "Charles Zhang"
__time__ = "2020-06-18 17:21"

import gym
from gym import spaces

START = (0, 0)
END = (0, 0)


class GridWorldEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, world_size):
        self.BOARD_ROWS = world_size[0]
        self.BOARD_COLS = world_size[1]
        self.action_space = spaces.Discrete(n=4)
        self.moves = {
                0: "up",
                1: "down",
                2: "left",
                3: "right"}

    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self, mode='human', close=False):
        pass


class GridWorld3x3(GridWorldEnv):

    def __init__(self):
        super(GridWorld3x3, self).__init__(world_size=(3, 3))


class GridWorld3x4(GridWorldEnv):

    def __init__(self):
        super(GridWorld3x4, self).__init__(world_size=(3, 4))


class GridWorld4x5(GridWorldEnv):

    def __init__(self):
        super(GridWorld4x5, self).__init__(world_size=(4, 5))


class GridWorld7x8(GridWorldEnv):

    def __init__(self):
        super(GridWorld7x8, self).__init__(world_size=(7, 8))

