__author__ = "Charles Zhang"
__time__ = "2020-07-01 16:15"

import numpy as np

V = 9
S = list(range(9))
"""
     Environment
      7 - 8 - 9
      4 - 5 - 6
      1 - 2 - 3
"""
alpha = 0.5
START = 0
END = 8
episodes = 100

R = [[-1, 0, -1, 0, -1, -1, -1, -1, -1],
     [0, -1, 0, -1, 0, -1, -1, -1, -1],
     [-1, 0, -1, -1, -1, 0, -1, -1, -1],
     [0, -1, -1, -1, 0, -1, 0, -1, -1],
     [-1, 0, -1, 0, -1, 0, -1, 0, -1],
     [-1, -1, 0, -1, 0, -1, -1, -1, 5],
     [-1, -1, -1, 0, -1, -1, -1, 0, -1],
     [-1, -1, -1, -1, 0, -1, 0, -1, 5],
     [-1, -1, -1, -1, -1, 0, -1, 0, -1]]


Q = np.zeros([V, V])


def get_actions(state):
    space = []
    for i in S:
        if R[state][i] != -1:
            space.append(i)
    return space


r = 1
while r <= episodes:
    s = np.random.choice(S)
    while True:
        # a = random a valid in the current state S
        action_space = get_actions(s)
        a = np.random.choice(action_space)
        # S' =a
        s_next = a
        # get Q(S' ,a')
        next_space = get_actions(s_next)
        qs = []
        for i in next_space:
            qs.append(Q[s_next][i])
        Q[s][a] = R[s][a] + round(alpha * max(qs), 3)
        # S = S'
        s = s_next
        if s == END:
            break
    r += 1

print(Q)

for i in range(V):
    for j in range(V):
        if Q[i][j] == 0:
            Q[i][j] = 100


path = []
state = 0

while len(path) < V:
    pre_state = state
    path.append(state)
    state = list(Q[state]).index(min(Q[state]))
    for i in range(V):
        Q[pre_state][i] = 100
        Q[i][pre_state] = 100

print(path)

