__author__ = "Charles Zhang"
__time__ = "2020-07-05 13:39"

from Graph_Based_Coverage import rl_MDP
from Graph_Based_Coverage import rl_MDP_greedy
from Graph_Based_Coverage import Graph

"""
 0   1   2   3   4   5   6   7
 8   9  10  11  12  13  14  15
16  17  18  19  20  21  22  23
24  25  26  27  28  29  30  31
32  33  34  35  36  37  38  39
40  41  42  43  44  45  46  47
48  49  50  51  52  53  54  55
"""
g = Graph.Graph(56)
g.create_gridworld(7, 8)


def gw7x8():
    agent = rl_MDP.RL_MDP(G=g)
    agent.train(l='non-TD')     # better to use simple bellman equation if no greedy move
    agent.show_path()


def gw7x8_greedy():
    agent = rl_MDP_greedy.RL_MDP(G=g)
    agent.train(rounds=1000, l='non-TD')
    agent.show_path()


if __name__ == '__main__':
    gw7x8()
    gw7x8_greedy()
