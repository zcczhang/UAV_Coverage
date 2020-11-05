import numpy as np
from find_moves import find_moves_hexagons
import gym


class HexagonEnv(gym.Env):

    def __init__(self, BOARD_ROWS, BOARD_COLS, side_length: float= 40):
        self.BOARD_ROWS = BOARD_ROWS
        self.BOARD_COLS = BOARD_COLS
        super(HexagonEnv, self).__init__()
        self.board = np.zeros([BOARD_ROWS + 1, BOARD_COLS + 1])  # I add one here to give the longer columns space
        self.state = (0, 0)
        #self.action_space = spaces.Discrete(4)  # I am not really using this stuff right now.
        self.visited = set()
        self.visited.add(tuple(self.state))
        self.side_length = side_length  # for rendering
        self.win = None  # for rendering


    def reset(self, pos = (0,0)):
        self.state = pos
        self.visited = set()
        self.visited.add(tuple(self.state))

    def action_space(self):
        return find_moves_hexagons(self.state, self.BOARD_ROWS, self.BOARD_COLS)

    def next_position(self, move):
        next_position = list(self.state)  # current position to be updated
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
        return next_position

    def step(self, move):
        self.state = self.next_position(move)
        self.visited.add(tuple(self.state))

    def is_end(self):
        to_subtract = (self.BOARD_ROWS - 1)//2 + 1  # how many short columns
        if len(self.visited) == self.BOARD_ROWS*self.BOARD_COLS - to_subtract:
            return True

    def give_reward(self):  # adding reward function in the environment
        if tuple(self.state) in self.visited:
            return -1
        else:
            return 1


if __name__ == "__main__":
    BOARD_ROWS = 5
    BOARD_COLS = 3
    env = HexagonEnv(BOARD_ROWS, BOARD_COLS)
    env.state = [3,0]
    # env.step('down_right')
    env.step('up_right')
    #print(env.give_reward())
    print(env.state)

