import gym
import numpy as np
from gym import spaces


class hexagonGymEnv(gym.Env):
    """
    my gym hexagon environment
    """

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.action_space = spaces.Discrete(6)
        self.actions = ['up', 'down', 'up_left', 'up_right', 'down_left', 'down_right']

        self.observation_space = spaces.Box(low=0,
                                            high=2,
                                            shape=(self.rows * self.cols,),
                                            dtype='uint8')
        self.board = np.zeros([rows, cols])
        self.pos = (0, 0)
        self.visited = set()
        self.visited.add(tuple(self.pos))

    def reset(self, pos=(0,0)):
        """ resets the board """
        self.pos = pos
        self.visited = set()
        self.visited.add(tuple(self.pos))
        return self.return_obs()

    def return_obs(self):
        """ returns the observation vector 0: unvisited, 1: visited, 2: agent pos"""
        obs = np.zeros(self.rows*self.cols)
        for visited in self.visited:
            index = visited[0]*self.cols + visited[1]
            obs[index] = 1
        index = self.pos[0] * self.cols + self.pos[1]
        obs[index] = 2
        return obs

    def next_position(self, action):
        """
        has the rules of where everything needs to go, and also binds the guys within the size of the board.
        :param move:
        :return:
        """
        move = self.actions[action]
        next_position = list(self.pos)  # current position to be updated
        if move == 'up':
            next_position[0] -= 1
        if move == 'down':
            next_position[0] += 1
        if move == 'up_left':
            if next_position[1] % 2 == 1:
                next_position[0] -= 1
            next_position[1] -= 1
        if move == 'up_right':
            if next_position[1] % 2 == 1:
                next_position[1] -= 1
            next_position[1] += 1
        if move == 'down_left':
            if next_position[1] % 2 == 0:
                next_position[0] += 1
            next_position[1] -= 1
        if move == 'down_right':
            if next_position[1] % 2 == 0:
                next_position[0] += 1
            next_position[1] += 1

        if next_position[1] % 2 == 0 and next_position[0] > self.rows - 2:
            next_position[0] = self.rows - 2
        if next_position[1] % 2 == 1 and next_position[0] > self.rows - 1:
            next_position[0] = self.rows - 1
        if next_position[1] > self.cols - 1:
            next_position[1] = self.cols - 1
        if next_position[1] < 0:
            next_position[1] = 0
        if next_position[0] < 0:
            next_position[0] = 0

        return next_position

    def get_reward(self):
        """ gives reward for most current position """
        if tuple(self.pos) in self.visited:
            return -1
        if tuple(self.pos) not in self.visited:
            return 1

    def step(self, action):
        """ stepss based on action and returns values"""
        self.pos = self.next_position(action)
        self.visited.add(tuple(self.pos))
        return self.return_obs(), self.get_reward(), self.is_end(), {}

    def render(self):
        print(self.return_obs())

    def is_end(self):
        """ returns a boolean of whether or not everything has been visited (is end or not)"""
        to_subtract = (self.rows - 1)//2 + 1  # how many short columns
        if len(self.visited) == self.rows*self.cols - to_subtract:
            return True
        return False

if __name__=="__main__":
    env = hexagonGymEnv(5,5)
    env.reset()
    for i in range(50):
        action = np.random.choice(range(6))
        env.step(action)
    env.render()
