from Double_Q_Learning.hexagon_env import HexagonEnv
from Double_Q_Learning.find_moves import find_moves_hexagons
import numpy as np
import matplotlib.pyplot as plt
import time
from Double_Q_Learning.ag_helper_functions import *

"""
A class that contains the logic to have two agents run together but this time it controls the teo agents at the same
time (i.e action is is both their moves)
"""


class DoubleHexagonAgent:

    def __init__(self, BOARD_ROWS, BOARD_COLS):
        self.env0 = HexagonEnv(BOARD_ROWS, BOARD_COLS)  # initializes environment inside agent class
        self.env1 = HexagonEnv(BOARD_ROWS, BOARD_COLS)

        self.BOARD_ROWS = BOARD_ROWS
        self.BOARD_COLS = BOARD_COLS

        self.combined_visited = set()

        self.alpha = 0.07
        self.exp_rate = 1
        self.decay_gamma = 0.9

        # for the graph 7/20
        self.total_reward = 0

        self.Q_values = {}  # initializes the q table
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                for ii in range(BOARD_ROWS):
                    for jj in range(BOARD_COLS):
                        self.Q_values[(i, j, ii, jj)] = {}
                        possible_moves_0 = find_moves_hexagons([i, j], BOARD_ROWS, BOARD_COLS)
                        for a_0 in possible_moves_0:
                            possible_moves_1 = find_moves_hexagons([ii, jj], BOARD_ROWS, BOARD_COLS)
                            for a_1 in possible_moves_1:
                                self.Q_values[(i, j, ii, jj)][(a_0, a_1)] = 0

    def give_reward_combined(self):  # adding reward function in the environment
        reward = 0
        if tuple(self.env0.state) in self.combined_visited:
            reward -= 2
        else:
            reward += 1
        if tuple(self.env1.state) in self.combined_visited:
            reward -= 2
        else:
            reward += 1
        return reward

    def is_end_multi(self):
        """
        checks whether or not the combined visited is filled out
        :return: boolean whether or not its over
        """
        to_subtract = (self.BOARD_ROWS - 1)//2 + 1  # how many short columns
        if len(self.combined_visited) == self.BOARD_ROWS*self.BOARD_COLS - to_subtract:
            return True
        return False

    def reset_all(self):
        """
        resets both of the environments
        """
        self.combined_visited = set()
        self.env0.reset(pos=(0, 0))
        self.env1.reset(pos=(self.BOARD_ROWS - 2, self.BOARD_COLS - 1))
        self.total_reward = 0
        # self.env1.reset(pos=(0, 1))
        #
        # self.env0.reset(pos=(2, 1))
        # self.env1.reset(pos=(2, 2))


    def optimal_action(self):
        # greedy move
        max_value = -10000
        action = ""
        combined_position = (self.env0.state[0], self.env0.state[1], self.env1.state[0], self.env1.state[1])
        # possible_actions = self.env0.action_space() + self.env1.action_space()
        for a in self.Q_values[combined_position]:
            next_value = self.Q_values[combined_position][a]
            if next_value >= max_value:
                action = a
                max_value = next_value
        return action


    def get_action(self):
        """
        Gets random action (with some fancy rules) or the optimal action
        """
        combined_position = (self.env0.state[0], self.env0.state[1], self.env1.state[0], self.env1.state[1])
        action_space = list(self.Q_values[combined_position].keys())
        if np.random.uniform(0, 1) <= self.exp_rate:  # exploration rate % of the time
            return action_space[np.random.choice(range(len(action_space)))]  # random selection
        else:
            return self.optimal_action()

    def set_action(self, action):  # sets and learns (this should probably be updated)
        curr_state_0 = self.env0.state
        curr_state_1 = self.env1.state
        combined_curr_position = (curr_state_0[0], curr_state_0[1], curr_state_1[0], curr_state_1[1])
        self.combined_visited.add(tuple(curr_state_0))
        self.combined_visited.add(tuple(curr_state_1))
        next_state_0 = self.env0.next_position(action[0])
        next_state_1 = self.env1.next_position(action[1])
        self.env0.state = next_state_0
        self.env1.state = next_state_1
        combined_next_position = (self.env0.state[0], self.env0.state[1], self.env1.state[0], self.env1.state[1])
        reward = self.give_reward_combined()
        self.total_reward += reward
        qs_of_next_state = []
        for q_value in self.Q_values[combined_next_position]:
            qs_of_next_state.append(self.Q_values[combined_next_position][q_value])
        delta = self.alpha*(reward + self.decay_gamma*(max(qs_of_next_state)) -
                            self.Q_values[combined_curr_position][action])
        self.Q_values[combined_curr_position][action] = round(self.Q_values[combined_curr_position][action]+delta, 4)

    def train(self, rounds=100):
        print("Training...")
        steps = []
        rewards = []
        for r in range(rounds):
            if r % 100 == 0:
                print(r)
            print(r)
            self.reset_all()
            self.exp_rate *= 0.9  # reduces the exploration rate every turn
            step = 0
            while True:
                #print(step)
                #print(self.combined_visited)
                #print(self.Q_values)
                # print(self.get_env_object(agent_index).state)
                action = self.get_action()
                #print(action)
                self.set_action(action)
                step += 1
                if self.is_end_multi():
                    break
            rewards.append(self.total_reward)
            steps.append(step)
        print("Training finished!")
        return steps, rewards

    def show_paths(self, final_steps):
        path0 = []
        path1 = []
        self.reset_all()
        for i in range(final_steps):
            path0.append(self.env0.state)
            path1.append(self.env1.state)
            action = self.optimal_action()  # the two actions
            self.env0.state = self.env0.next_position(action[0])
            self.env1.state = self.env1.next_position(action[1])
        return path0, path1

def when_converge(steps_list, limit=10):
    """
    an analysis function (finds the step that it converges on)
    :param steps_list: in a list how far do you have to go to find repeating elements (usually this means convergence)
    :param limit:
    :return:
    """
    current = -1  # set to negative one because none will be this ever.
    same = 0  # how many times the same number has been visited
    for i in range(len(steps_list)):
        steps = steps_list[i]
        if steps == current:
            same += 1
        else:
            current = steps
        if same == limit:
            return i - limit


def get_single_path(tup_path, cols):
    single_path = []
    for i in tup_path:
        single_path.append(tuple_to_single_index(i, cols))
    return single_path


if __name__ == "__main__":
    rows = 5
    cols = 5

    agents = DoubleHexagonAgent(rows, cols)
    agents.reset_all()

    steps, rewards = agents.train(rounds=5000)
    # agents.show_path(0)
    print()
    # agents.show_path(1)
    print()
    # print(agents.Q_values)
    print(steps)
    when_converge = when_converge(steps)
    print(when_converge)
    final_steps = steps[len(steps)-1]
    print(final_steps)
    path0, path1 = agents.show_paths(final_steps)
    print(path0)
    print(path1)
    print(get_single_path(path0, cols))
    print(get_single_path(path1, cols))

    plt.plot(rewards)
    plt.show()
