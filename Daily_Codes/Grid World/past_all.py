__author__ = "Charles Zhang"
__time__ = "2020-06-15 21:36" 
 
import numpy as np
BOARD_ROWS = 3
BOARD_COLS = 4
START = (0, 0)
END = (2, 3)


class State:

    def __init__(self, state=START):
        self.board = np.zeros([BOARD_ROWS, BOARD_COLS])
        self.state = state    # tuple of the coordinate
        self.is_end = False
        self.is_past = False

    def give_reward(self):
        reward = 0
        if self.is_past:
            reward -= .1
        else:
            reward += .1
        return reward

    def check_end(self):
        if self.state == END:
            self.is_end = True

    def next_position(self, action):
        if action == "up":
            next_state = (self.state[0] - 1, self.state[1])
        elif action == "down":
            next_state = (self.state[0] + 1, self.state[1])
        elif action == "left":
            next_state = (self.state[0], self.state[1] - 1)
        else:
            next_state = (self.state[0], self.state[1] + 1)
        if (next_state[0] >= 0) and (next_state[0] < BOARD_ROWS):
            if (next_state[1] >= 0) and (next_state[1] < BOARD_COLS):
                return next_state
        return self.state


class Agent:

    def __init__(self):
        self.actions = ["up", "down", "left", "right"]  # space
        self.State = State()
        self.is_end = self.State.is_end
        self.alpha = 0.3
        self.exp_rate = 1
        self.decay_gamma = 0.9
        self.Q_values = {}  # init Q values (dict)
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                self.Q_values[(i, j)] = {}
                for a in self.actions:
                    self.Q_values[(i, j)][a] = 0
        self.past_all = []
        for i in range(BOARD_ROWS):
            t = []
            for j in range(BOARD_COLS):
                t.append(False)
            self.past_all.append(t)

    def get_action(self):
        max_value = 0
        action = ""
        if np.random.uniform(0, 1) <= self.exp_rate:
            action = np.random.choice(self.actions)
        else:
            # greedy action
            for a in self.actions:
                next_value = self.Q_values[self.State.state][a]
                if next_value >= max_value:
                    action = a
                    max_value = next_value
        return action

    def set_action(self, action):
        curr_state = self.State.state
        self.State.is_past = True
        next_state = self.State.next_position(action)
        self.State = State(state=next_state)
        reward = self.State.give_reward()
        if next_state == END and self.check_all_past:
            reward += 1
        if self.past_all[next_state[0]][next_state[1]] is False:
            self.State.is_past = True
            self.past_all[next_state[0]][next_state[1]] = True

        qs_of_next_state = []
        for q_value in self.Q_values[next_state]:
            qs_of_next_state.append(self.Q_values[next_state][q_value])
        delta = self.alpha * (reward + self.decay_gamma * (max(qs_of_next_state)) -
                              self.Q_values[curr_state][action])
        self.Q_values[curr_state][action] = round(self.Q_values[curr_state][action] + delta, 5)

    def reset(self):
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                self.past_all[i][j] = False
                self.State = State(state=(i, j))
                self.State.is_past = False
        self.State = State()
        self.is_end = self.State.is_end

    def check_all_past(self):
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if self.past_all[i][j] is True:
                    return True
        return False

    def train(self, rounds=50):
        print("Training...")
        for r in range(rounds):
            self.reset()
            while (not self.is_end) and (not self.check_all_past):
                action = self.get_action()
                self.set_action(action)
                self.State.check_end()
                self.is_end = self.State.is_end
        print("Training finished!")


agent = Agent()
agent.train()
print(agent.Q_values)