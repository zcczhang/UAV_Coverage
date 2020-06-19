__author__ = "Charles Zhang"
__time__ = "2020-06-18 17:21"

import gym
import numpy as np
from gym import spaces

START = (0, 0)
END = (0, 0)


class GridWorldEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, world_size, state=START):
        self.BOARD_ROWS = world_size[0]
        self.BOARD_COLS = world_size[1]
        self.state = state      # tuple of the coordinate
        self.is_end = False

        self.action_space = spaces.Discrete(n=4)
        self.moves = {
                0: "up",
                1: "down",
                2: "left",
                3: "right"}

        self.State = state
        self.is_end = False

        self.alpha = 0.3  # learning rate
        self.exp_rate = 1  # epsilon-greedy parameter
        self.decay_gamma = 0.9

        self.Q_values = {}  # init Q table (dict)
        for i in range(self.BOARD_ROWS):
            for j in range(self.BOARD_COLS):
                self.Q_values[(i, j)] = {}
                for a in range(self.action_space.n):
                    self.Q_values[(i, j)][self.moves[a]] = 0

        # init a list to check if each grid is past
        self.past_all = np.zeros((self.BOARD_ROWS, self.BOARD_COLS), dtype=bool)

        self.step = 0  # step for each episode

    def _next_position(self, action):
        """
        :return: next state
        """
        if action == 1:
            next_state = (self.state[0] - 1, self.state[1])
        elif action == 2:
            next_state = (self.state[0] + 1, self.state[1])
        elif action == 3:
            next_state = (self.state[0], self.state[1] - 1)
        else:
            next_state = (self.state[0], self.state[1] + 1)
        # boundary condition
        if (next_state[0] >= 0) and (next_state[0] < self.BOARD_ROWS):
            if (next_state[1] >= 0) and (next_state[1] < self.BOARD_COLS):
                return next_state
        return self.state

    def step(self, action):
        next_state = self._next_position(action)

    def optimal_action(self):
        # greedy move
        max_value = -10000
        action = ""
        for a in range(self.action_space.n):
            next_value = self.Q_values[self.State.state][self.moves[a]]
            if next_value >= max_value:
                action = a
                max_value = next_value
        return action

    def get_action(self):
        """
        The agent should choose randomly among the positions that have
        not been visited, and if all possible positions are visited,
        then move randomly and receive a negative reward
        """
        if np.random.uniform(0, 1) <= self.exp_rate:
            # Get four potential positions of the current state
            up = self.State.next_position("up")
            down = self.State.next_position("down")
            left = self.State.next_position("left")
            right = self.State.next_position("right")
            # Check if all potential positions are visited
            rule = [self.past_all[up[0]][up[1]] is True,
                    self.past_all[down[0]][down[1]] is True,
                    self.past_all[left[0]][left[1]] is True,
                    self.past_all[right[0]][right[1]] is True]
            # If all are visited, return a random action
            if all(rule):
                return self.action_space.sample()
            # Else try to get an available unvisited position randomly
            else:
                while True:
                    action = np.random.choice(self.actions)
                    next_state = self.State.next_position(action)
                    if self.past_all[next_state[0]][next_state[1]] is False:
                        return action
                    else:
                        continue
        else:
            return self.optimal_action()

    def give_reward(self):
        """
        + 1 reward for visiting the unvisited grid
        -.1 reward for visiting the visited grid
        """
        reward = 0
        if self.past_all[self.State.state[0]][self.State.state[1]] is False:
            reward += 1
        else:
            reward -= .1
        return reward

    def set_action(self, action):
        # set current stat past
        curr_state = self.State.state
        self.past_all[curr_state[0]][curr_state[1]] = True
        # get the next state
        next_state = self.State.next_position(action)
        self.State = State(state=next_state)
        reward = self.give_reward()
        # set the next state past
        if self.past_all[next_state[0]][next_state[1]] is False:
            self.past_all[next_state[0]][next_state[1]] = True
        # give the global reward if finish an epsiode
        if self.State.state == START and self.check_all_past():
            reward += 1
        # update the Q table
        qs_of_next_state = []
        for q_value in self.Q_values[next_state]:
            qs_of_next_state.append(self.Q_values[next_state][q_value])
        delta = self.alpha * (reward + self.decay_gamma * (max(qs_of_next_state)) -
                              self.Q_values[curr_state][action])
        self.Q_values[curr_state][action] = round(self.Q_values[curr_state][action] + delta, 4)

    def reset(self):
        for i in range(self.BOARD_ROWS):
            for j in range(self.BOARD_COLS):
                self.past_all[i][j] = False
        self.State = State()
        self.is_end = self.State.is_end

    def check_all_past(self):
        for i in self.past_all:
            for j in i:
                if j is False:
                    return False
        return True

    def check_end(self):
        if self.state == END:
            self.is_end = True

    def render(self, mode='human', close=False):
        pass

    def show_path(self, q_values):
        """
        demo:
        -------------------------
        |  down  | down  | left |
        -------------------------
        |  down  | left  |  up  |
        -------------------------
        |  right | right |  up  |
        -------------------------
        """
        for i in range(self.BOARD_ROWS):
            print('---------------------------------------')
            row_string = "| "
            for j in range(self.BOARD_COLS):
                best_val = -1000
                best_move = ""
                for a in q_values[(i, j)]:
                    if q_values[(i, j)][a] > best_val:
                        best_val = q_values[(i, j)][a]
                        best_move = a
                row_string = row_string + " " + best_move + " |"
            print(row_string)
        print('---------------------------------------')


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

