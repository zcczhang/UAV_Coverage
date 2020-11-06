import numpy as np
from multi_agent_Q_Learning.find_moves import find_moves_squares
import gym


class GridEnv(gym.Env):

    def __init__(self, BOARD_ROWS, BOARD_COLS, side_length: float = 40):
        self.BOARD_ROWS = BOARD_ROWS
        self.BOARD_COLS = BOARD_COLS
        super(GridEnv, self).__init__()
        self.board = np.zeros([BOARD_ROWS + 1, BOARD_COLS + 1])  # add one here to give the longer columns space
        self.state = (0, 0)
        self.visited = set()
        self.visited.add(tuple(self.state))
        self.side_length = side_length  # for rendering
        self.win = None  # for rendering

    def reset(self, pos=(0, 0)):
        self.state = pos
        self.visited = set()
        self.visited.add(tuple(self.state))

    def action_space(self):
        return find_moves_squares(self.state, self.BOARD_ROWS, self.BOARD_COLS)

    def next_position(self, move):
        next_position = list(self.state)  # current position to be updated
        if move == 'up':
            next_position[0] -= 1
        if move == 'down':
            next_position[0] += 1
        if move == 'left':
            next_position[1] -= 1
        if move == 'right':
            next_position[1] += 1
        return next_position

    def step(self, move):
        self.state = self.next_position(move)
        self.visited.add(tuple(self.state))

    def is_end(self):
        if len(self.visited) == self.BOARD_ROWS*self.BOARD_COLS:
            return True

    def give_reward(self):  # adding reward function in the environment
        if tuple(self.state) in self.visited:
            return -1
        else:
            return 1


if __name__ == "__main__":
    BOARD_ROWS = 5
    BOARD_COLS = 3
    env = GridEnv(BOARD_ROWS, BOARD_COLS)
    env.state = [3, 0]
    env.step('right')
    print(env.state)

