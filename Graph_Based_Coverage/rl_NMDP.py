__author__ = "Charles Zhang"
__time__ = "2020-07-05 15:55"

import numpy as np
import datetime


class RL:

    def __init__(self, G,
                 START=0,
                 END=1,
                 REWARD=100,
                 alpha=0.1,         # learning rate
                 decay_gamma=0.6):  # discount factor
        self.START = START
        self.END = END
        self.alpha = alpha
        self.decay_gamma = decay_gamma
        self.reward = REWARD
        self.G = G                          # Graph representation
        self.V = G.V                        # number of vertices V
        self.R = self.get_R()               # Reward Matrix
        self.S = list(range(self.V))        # State space
        self.Q = np.zeros([self.V, self.V])      # initialize Q table
        self.past_all = [False] * self.V    # list to observe if S is past

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

    def check_past(self):
        return self.past_all == [True] * self.V

    def train(self, rounds=500):
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

        # TODO

        end_time = datetime.datetime.now()
        print('\r{0}'.format("100%|==========|100%"))
        print("Running Time(s): ", (end_time - start_time).total_seconds())

    # TODO
    def show_path(self):

        pass

