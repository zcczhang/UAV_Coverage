__author__ = "Charles Zhang"
__time__ = "2020-07-03 11:00"


class Graph(object):
    """
    Graph representation in Python
    """

    def __init__(self, V):
        self.adjMatrix = []  # initialize the adjacency matrix of G(V,E)
        for i in range(V):
            self.adjMatrix.append([0 for i in range(V)])
        self.V = V  # number of vertices

    def add_edge(self, v1, v):
        """
        :param v1: a vertex
        :param v: a list of vertices connected to v1
        """
        for v2 in v:
            if v1 == v2:
                return
            self.adjMatrix[v1][v2] = 1
            self.adjMatrix[v2][v1] = 1

    def check_connected(self, v1, v2):
        """
        :return: True if v1 v2 connected
        """
        return self.adjMatrix[v1][v2] != 0

    def create_gridworld(self, R, C):
        """
        Graph representation of the Grid World

           0 --- 1 -- ... -- C
           |     |    ...    |
          C+1 - C+2 - ... - 2*C+1
           .     .    ...    .
           .     .    ...    .
           .     .    ...    .
        (R-1)*C  .    ... - R*C-1

        :param R: number of rows
        :param C: number of columns
        """
        g = Graph(R * C)
        for i in range(R - 1):
            # connect vertices in the right first column
            g.add_edge((i + 1) * C - 1, [(i + 2) * C - 1])
            for j in range(C - 1):
                # connect vertices
                g.add_edge(j + i * C, [j + i * C + 1, j + i * C + C])
        # connect vertices in the last row
        for i in range(C - 1):
            g.add_edge(R * C - 2 - i, [R * C - 1 - i])
        self.adjMatrix = g.adjMatrix
        self.V = g.V

    def __len__(self):
        return self.V
