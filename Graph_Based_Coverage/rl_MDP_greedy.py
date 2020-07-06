__author__ = "Charles Zhang"
__time__ = "2020-07-06 12:42"

import numpy as np
import datetime


class RL_MDP:
    """
    Markov Decision Process(MDP) Q learning algorithm
    with Graph-based representation
    """

    def __init__(self, G,
                 START=0,
                 END=1,
                 REWARD=100,
                 alpha=0.3,         # learning rate
                 decay_gamma=0.9,   # discount factor
                 exp_rate=0.5):       # e-greedy parameter
        self.START = START
        self.END = END
        self.alpha = alpha
        self.decay_gamma = decay_gamma
        self.exp_rate = exp_rate
        self.reward = REWARD
        self.G = G                          # Graph representation
        self.V = G.V                        # number of vertices V
        self.R = self.get_R()               # Reward Matrix
        self.S = list(range(self.V))        # State space
        self.Q = np.zeros([self.V, self.V])      # initialize Q table

    def get_R(self):
        R = self.G.adjMatrix
        for i in range(self.V):
            if self.G.check_connected(i, self.END):
                R[i][self.END] = self.reward    # set the rewarding move
        return R

    def get_action_space(self, s):
        actions = []
        for i in range(self.V):
            if self.G.check_connected(s, i):    # filter the possible movements
                actions.append(i)               # equivalently, vertices are connected
        return actions

    def get_action(self, s):
        """
        Greedy_Move
        """
        if np.random.uniform(0, 1) <= self.exp_rate:
            if max(self.Q[s]) > 0:
                return list(self.Q[s]).index(max(self.Q[s]))
        action_space = self.get_action_space(s)
        return np.random.choice(action_space)

    def train(self, rounds=500, l="TD"):
        """
        :param rounds: training total episodes
        :param l: value update method, temporal difference(TD)
                  or simple bellman equation

        """
        print("Training...")
        start_time = datetime.datetime.now()
        # progress bar
        for r in range(rounds):
            t = str(round(r / (rounds / 10) * 10)) + '%|'
            for i in range(int(r / (rounds / 10))):
                t += '='
            for i in range(int(10 - r / (rounds / 10)) + 1):
                t += ' '
            print('\r{0}'.format(t + '|100%'), end="")
            s = np.random.choice(self.S)
            while True:
                action = self.get_action(s)
                s_next = action
                actions_next = self.get_action_space(s_next)
                qs = []
                for a in actions_next:
                    qs.append(self.Q[s_next][a])
                if l == 'TD':
                    self.Q[s][action] += self.alpha * (self.R[s][action] +                  # temporal difference(TD)
                                                       self.decay_gamma * max(qs) -
                                                       self.Q[s][action])
                else:
                    self.Q[s][action] = self.R[s][action] + self.decay_gamma * max(qs)      # simple bellman equation
                s = s_next
                if s == self.END:
                    break
        end_time = datetime.datetime.now()
        print('\r{0}'.format("100%|==========|100%"))
        print("Running Time(s): ", (end_time - start_time).total_seconds())

    def show_path(self):
        path = []
        for i in range(self.V):
            for j in range(self.V):
                if self.Q[i][j] == 0:
                    self.Q[i][j] = 1000     # can't calculate with NA so just give a big number
        state = self.START
        while len(path) < self.V:
            pre_state = state
            path.append(state)
            state = list(self.Q[state]).index(min(self.Q[state]))
            for i in range(self.V):
                self.Q[pre_state][i] = 1000
                self.Q[i][pre_state] = 1000
        path.append(self.START)
        print(path)

