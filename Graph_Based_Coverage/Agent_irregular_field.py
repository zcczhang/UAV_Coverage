__author__ = "Charles Zhang"
__time__ = "2020-07-08 01:33" 
 
from Graph_Based_Coverage import Graph
from Graph_Based_Coverage import rl_MDP


def main():
    """
    Test on an irregular field environment
    """
    g = Graph.Graph(18)
    g.add_edge(0, [1, 4])
    g.add_edge(1, [5])
    g.add_edge(2, [3, 7])
    g.add_edge(3, [4, 8])
    g.add_edge(4, [5, 9])
    g.add_edge(5, [6, 10])
    g.add_edge(6, [11])
    g.add_edge(7, [8, 12])
    g.add_edge(8, [9, 13])
    g.add_edge(9, [10])
    g.add_edge(10, [11, 14])
    g.add_edge(11, [15])
    g.add_edge(12, [13])
    g.add_edge(14, [15, 16])
    g.add_edge(15, [17])
    g.add_edge(16, [17])
    agent = rl_MDP.RL_MDP(G=g, alpha=0.1, decay_gamma=0.9)    # still trying to find the best parameters to
    agent.train(rounds=1000)                                  # let the possibility to converge increases
    agent.show_path()


if __name__ == '__main__':
    main()
