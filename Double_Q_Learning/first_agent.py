from Double_Q_Learning.hexagon_env import HexagonEnv
from Double_Q_Learning.find_moves import find_moves_hexagons
import numpy as np
import time


class HexagonAgent:

    def __init__(self, BOARD_ROWS, BOARD_COLS):
        self.env = HexagonEnv(BOARD_ROWS, BOARD_COLS)  # initializes environment inside agent class

        self.alpha = 0.3
        self.exp_rate = 1
        self.decay_gamma = 0.9

        # self.alpha = 0.5
        # self.exp_rate = .99
        # self.decay_gamma = 0.8

        self.Q_values = {}  # initializes the q table
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                self.Q_values[(i, j)] = {}
                possible_moves = find_moves_hexagons([i, j], BOARD_ROWS, BOARD_COLS)
                for a in possible_moves:
                    self.Q_values[(i, j)][a] = 0  # fills it out with zeros

    def optimal_action(self):
        # greedy move
        max_value = -10000
        action = ""
        possible_actions = self.env.action_space()
        for a in possible_actions:
            next_value = self.Q_values[tuple(self.env.state)][a]
            if next_value >= max_value:
                action = a
                max_value = next_value
        return action


    def get_action(self):
        """
        Gets random action (with some fancy rules) or the optimal action
        """
        action_space = self.env.action_space()
        if np.random.uniform(0, 1) <= self.exp_rate:  # exploration rate % of the time
            return np.random.choice(action_space)
            # print('random move')
            # rule = True
            # for move in self.env.action_space():
            #     close_by = self.env.next_position(move)  # loops through all close by positions
            #     rule = rule and (tuple(close_by) not in self.env.visited)  # decides if those positions are visited
            # if rule:
            #     return np.random.choice(action_space)  # if all have been visited, visit a random one
            # else:
            #     while True:
            #         action = np.random.choice(action_space)  # pick a random action
            #         if tuple(self.env.next_position(action)) in self.env.visited:  # make sure it hasn't been visited
            #             return action
        else:
            return self.optimal_action()

    def set_action(self, action):  # sets and learns (this should probably be updated)
        curr_state = self.env.state
        self.env.visited.add(tuple(curr_state))
        # self.past_all[curr_state[0]][curr_state[1]] = True
        next_state = self.env.next_position(action)
        self.env.state = next_state
        #print('setting next state to: ' + str(next_state))
        reward = self.env.give_reward()
        # if self.past_all[next_state[0]][next_state[1]] is False:  # I don't think I need this part from Charles' code
        #     self.past_all[next_state[0]][next_state[1]] = True
        qs_of_next_state = []
        for q_value in self.Q_values[tuple(next_state)]:
            qs_of_next_state.append(self.Q_values[tuple(next_state)][q_value])
        delta = self.alpha*(reward + self.decay_gamma*(max(qs_of_next_state)) -
                            self.Q_values[tuple(curr_state)][action])
        self.Q_values[tuple(curr_state)][action] = round(self.Q_values[tuple(curr_state)][action]+delta, 4)

    def train(self, rounds=100):
        print("Training...")
        steps = []
        for r in range(rounds):
            self.env.reset()
            self.exp_rate *= 0.9  # reduces the exploration rate every turn
            step = 0
            while True:
                #print(step)
                action = self.get_action()
                self.set_action(action)
                step += 1
                if self.env.is_end():
                    break
            steps.append(step)
        print("Training finished!")
        return steps


    def show_path(self):
        direction_dict = {'up': 1,
                          'up_right': 2,
                          'down_right': 3,
                          'down': 4,
                          'down_left': 5,
                          'up_left': 6}

        for i in range(self.env.BOARD_ROWS):
            row_string = ""
            for j in range(self.env.BOARD_COLS):
                self.env.state = (i, j)
                best_move = self.optimal_action()
                if i != self.env.BOARD_ROWS - 1 or j % 2 == 1:
                    row_string = row_string + " " + str(direction_dict[best_move])
                else:
                    row_string = row_string + "  "

            print(row_string)


# an analysis function (finds the step that it converges on) - should work most of the time
def when_converge(steps_list, limit):
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


if __name__ == "__main__":
    rows = 4  # might want to find a smarter way to share this information between classes/ files
    cols = 3

    agent = HexagonAgent(rows, cols)
    steps = agent.train(rounds=400)
    print(steps)
    print(when_converge(steps, 10))
    agent.show_path()
    print(agent.Q_values)

    # maybe I just messed up the is_end