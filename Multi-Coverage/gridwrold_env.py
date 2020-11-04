import gym
from gym.utils import seeding
from gym import spaces
import numpy as np
from enum import IntEnum
from copy import deepcopy
from tabulate import tabulate


class Board:
    """Represent a grid and operations on it"""
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.data = np.zeros((height, width), dtype=np.int)

        self.total_grids = width * height
        self.visited_grids = 0

    def set(self, i, j):
        """
        Increment the visited counts in the grid
        :param i: row
        :param j: column
        """
        assert i >= 0 and i < self.height
        assert j >= 0 and j < self.width

        if self.data[i, j] == 0:    # Not visited
            self.visited_grids += 1

        self.data[i, j] += 1

        return self.data[i, j]

    def get(self, i, j):
        """
        Increment the visited counts in the grid
        :param i: row
        :param j: column
        :return:
        """
        assert i >= 0 and i < self.height
        assert j >= 0 and j < self.width
        return self.data[i, j]

    def is_valid(self, i, j):
        """Check if a position is in the boundary"""
        return 0 <= i < self.height and 0 <= j < self.width

    def is_filled(self):
        return self.total_grids == self.visited_grids

    def __str__(self):
        return str(self.data)


class GridworldEnv(gym.Env):
    """
    Gridworld Environment that represents a rectangle world
    """

    metadata = {'render.modes': ['human']}

    class Actions(IntEnum):
        left = 0
        right = 1
        up = 2
        down = 3

    def __init__(self, width, height, seed=1337):
        super(GridworldEnv, self).__init__()
        # self.world = np.array((width, height), dtype=int)

        # Environment configuration
        self.width = width
        self.height = height
        self.size = width * height

        # Information for the agent
        self.agent_pos = (0, 0)
        self.steps = [(0, 0)]
        self.board = Board(width, height)

        # For gym
        # Actions are discrete integer values
        self.action_space = spaces.Discrete(4)
        # Observations are number of cells
        self.observation_space = spaces.Box(low=-1, high=2,
                                            shape=(self.size, ), dtype=np.int)

        # Initialize the state
        self.reset()

        # Initialize the RNG
        self.seed(seed=seed)

        # Action enumeration for this environment
        self.actions = GridworldEnv.Actions

    def reset(self):
        # Current position and direction of the agent
        h = 0
        w = 0
        self.agent_pos = (h, w)

        self.board = Board(self.width, self.height)
        self.board.set(h, w)

        board = deepcopy(self.board.data)
        board[0, 0] = -1
        board = board.flatten()

        # Step count since episode start
        self.steps = [(0, 0)]

        # Return first observation
        return board.flatten()

    def seed(self, seed=1337):
        """
        Seed the random number generator
        """
        self.np_random, _ = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        done = False

        # Get the coordinate for the new position
        prev_i, prev_j = self.agent_pos
        i, j = self.agent_pos

        if action == self.actions.left:
            j -= 1
        elif action == self.actions.right:
            j += 1
        elif action == self.actions.up:
            i -= 1
        elif action == self.actions.down:
            i += 1

        if not self.board.is_valid(i, j):   # New position out of bound
            board = deepcopy(self.board.data)
            board[prev_i, prev_j] = -1
            board = board.flatten()
            return board, -1, False, {}

        self.agent_pos = (i, j)
        # Update the step information
        self.steps.append((i, j))
        self.board.set(i, j)
        board = deepcopy(self.board.data)
        board[i, j] = -1
        board = board.flatten()

        if self.board.get(i, j) > 1:   # The grid has been visited
            return board, 0, True, {}
        elif len(self.steps) >= self.size:  # All grids has been visited once
            return board, 100000, True, {}
        else:   # The grid has not been visited
            return board, 1, False, {}

    def render(self, mode='human', close=False):
        print("board:")
        print(self.board.data)
        print("path:", self.get_path())
        print("pos:", self.agent_pos)
        print("")

    def get_path(self):
        """
        Get the path on the field
        :return:
        """
        board = np.zeros((self.height, self.width), dtype=np.int)
        for index, pos in enumerate(self.steps):
            i, j = pos
            board[i, j] = index

        table = tabulate(board)
        return table

