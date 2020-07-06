__author__ = "Charles Zhang"
__time__ = "2020-07-03 11:06"

from Graph_Based_Coverage import Graph
from Graph_Based_Coverage import rl_MDP


def hex15():
    """
       1     3      5
    0     2     4
       7     9     11
    6     8    10
      12    13     14
    """
    g = Graph.Graph(15)
    g.add_edge(0, [1, 6, 7])
    g.add_edge(1, [0, 7, 2])
    g.add_edge(2, [3, 7, 8, 9])
    g.add_edge(3, [4, 9])
    g.add_edge(4, [5, 9, 10, 11])
    g.add_edge(5, [11])
    g.add_edge(6, [7, 12])
    g.add_edge(7, [8, 12])
    g.add_edge(8, [9, 12, 13])
    g.add_edge(9, [10, 13])
    g.add_edge(10, [11, 13, 14])
    g.add_edge(11, [14])

    agent = rl_MDP.RL_MDP(G=g)
    agent.train()       # better to use TD value update method
    agent.show_path()


if __name__ == '__main__':
    hex15()
