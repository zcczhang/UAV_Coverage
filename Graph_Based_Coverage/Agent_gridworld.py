__author__ = "Charles Zhang"
__time__ = "2020-07-05 13:39"

from Graph_Based_Coverage import rl_MDP
from Graph_Based_Coverage import Graph


def gw4x5():
    """
    0 — 1 — 2 — 3 — 4
    |   |   |   |   |
    5 — 6 — 7 — 8 — 9
    |   |   |   |   |
    10— 11— 12— 13— 14
    |   |   |   |   |
    15— 16— 17— 18— 19

    """
    g = Graph.Graph(20)
    g.create_gridworld(4, 5)
    agent = rl_MDP.RL_MDP(G=g)
    agent.train()
    agent.show_path()


if __name__ == '__main__':
    gw4x5()
