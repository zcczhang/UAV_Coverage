__author__ = "Charles Zhang"
__time__ = "2020-07-08 15:28" 


from Graph_Based_Coverage import Graph
from Graph_Based_Coverage import dual_agent_rl


"""
0  1  2  3
4  5  6  7
8  9  10 11
"""
g = Graph.Graph(12)
g.create_gridworld(3, 4)


def gw3x4_dual():
    agent = dual_agent_rl.RL_MDP(G=g, END=7)
    agent.train(rounds=500, l='TD')
    agent.show_path()


# """
#  0   1   2   3   4   5   6   7
#  8   9  10  11  12  13  14  15
# 16  17  18  19  20  21  22  23
# 24  25  26  27  28  29  30  31
# 32  33  34  35  36  37  38  39
# 40  41  42  43  44  45  46  47
# 48  49  50  51  52  53  54  55
# """
# g = Graph.Graph(56)
# g.create_gridworld(7, 8)


def gw7x8_dual():
    agent = dual_agent_rl.RL_MDP(G=g, START=24, END=31)
    agent.train(rounds=1000, l='nTD')
    agent.show_path()


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

    agent = dual_agent_rl.RL_MDP(G=g, START=0, END=9)
    agent.train(rounds=1000)       # better to use TD value update method
    agent.show_path()


if __name__ == '__main__':
    gw3x4_dual()
    # gw7x8_dual()
    hex15()
