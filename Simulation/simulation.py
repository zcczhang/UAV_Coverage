from graphics import *
from math import pi, cos, sin, sqrt
from multi_agent_Q_Learning.ag_helper_functions import tuple_to_single_index

"""
Credit to Aaron Gould, Elisabeth Landgren, and Fan Zhang who collaborate with me on this project
"""


def num_to_coord(num: int, cols: int):
    """
    (Inspired by aaron)
    takes in an integer that represents a cell on a square or hexagonal grid and returns the (i,j) coordinate

     # 0  1   2  3
     # 4  5   6  7
     # 8  9  10 11

     #     1     3      5
     # 0     2     4
     #    7     9     11
     # 6     8    10
     #    13    15     17

    :param num: single int
    :param cols: number of columns
    :return: an ordered pair
    """
    return (num // cols, num % cols)


def simulate_grid(rows, columns, path1, path2, side_length: int = 60, win=None, open_until_close=False,
                  slow_down: float = 0.2):
    """
    This function renders the paths of 2 agents in a square grid
    Agent1 = grey circle with  green path
    Agent2 = black circle with blue path
    red tile = both agents have been at that location

    ####NOTE: currently only supports when the paths are of equal length####

    :param rows: number of rows in grid
    :param columns: number of columns in grid
    :param path1: path of first agent can either be a list of coordinate tuples or integers
    :param path2: path of second agent can either be a list of coordinate tuples or integers
    :param side_length: optional int side_length of the square grid (default 60)
    :param win: optional window (default None will create window with grid lines)
    :param open_until_close: optional boolean(default False will close when all code has run) - True will stay open until click
    :param slow_down: optional float (default is 0.2 will slow down the animation by 0.2 seconds every time step)
    :return: window
    """

    # initializes the agents off screen to be animated

    circle1 = Circle(Point(-10, -10), side_length / 5)
    circle2 = Circle(Point(-10, -10), side_length / 5)

    # determines the whitespace for the color tiles

    buffer = 2

    win_width = side_length * columns
    win_height = side_length * rows

    # Creates new graphics window if none given and draws the grid
    if win is None:
        win = GraphWin('GridWorld', win_width, win_height)
        # draws black grid

        for i in range(rows + 1):
            for j in range(columns + 1):
                start_pt = Point(0, i * side_length)
                end_pt = Point(win_width, i * side_length)
                hline = Line(start_pt, end_pt)
                hline.setWidth(2)
                hline.draw(win)

                start_pt = Point(j * side_length, 0)
                end_pt = Point(j * side_length, win_height)
                vline = Line(start_pt, end_pt)
                vline.setWidth(2)
                vline.draw(win)

    path_length = max(len(path1), len(path2))

    # goes through each point in the paths of both agents and performs each action
    # NOTE: currently only supports when the paths are of equal length #

    for i in range(path_length):
        time.sleep(slow_down)
        agent1 = path1[i]
        agent2 = path2[i]

        coord1 = num_to_coord(agent1, columns)
        coord2 = num_to_coord(agent2, columns)

        x_1 = (coord1[1] + 1) * side_length - side_length / 2
        y_1 = (coord1[0] + 1) * side_length - side_length / 2

        x_2 = (coord2[1] + 1) * side_length - side_length / 2
        y_2 = (coord2[0] + 1) * side_length - side_length / 2

        circle1.undraw()
        circle2.undraw()

        circle1 = Circle(Point(x_1, y_1), side_length / 5)
        circle2 = Circle(Point(x_2, y_2), side_length / 5)
        circle1.setFill('grey')
        circle2.setFill('black')

        top_left_1 = Point(coord1[1] * side_length + buffer, coord1[0] * side_length + buffer)
        bottom_right_1 = Point((coord1[1] + 1) * side_length - buffer, (coord1[0] + 1) * side_length - buffer)

        top_left_2 = Point(coord2[1] * side_length + buffer, coord2[0] * side_length + buffer)
        bottom_right_2 = Point((coord2[1] + 1) * side_length - buffer, (coord2[0] + 1) * side_length - buffer)

        rect1 = Rectangle(top_left_1, bottom_right_1)
        rect2 = Rectangle(top_left_2, bottom_right_2)
        rect1.setWidth(0)
        rect2.setWidth(0)

        num_visits_1 = int(path1[0:i + 1].count(agent1) + path2[0:i + 1].count(agent1))
        num_visits_2 = int(path1[0:i + 1].count(agent2) + path2[0:i + 1].count(agent2))

        if num_visits_1 == 1:
            rect1.setFill("lightgreen")
        elif num_visits_1 > 1:
            rect1.setFill("red")

        if num_visits_2 == 1:
            rect2.setFill("lightblue")
        elif num_visits_2 > 1:
            rect2.setFill("red")

        rect1.draw(win)
        rect2.draw(win)
        circle1.draw(win)
        circle2.draw(win)

    # keeps window open if option selected
    if open_until_close:
        if win is not None:
            win.getMouse()
            win = None

    return win


def hexagon(x: float = 0, y: float = 0, side_length: float = 40, fill=None):
    " This function takes in sidelength and x,y coordinates corresponding to the center of a hexagon, default is a 40 sidelength hex at 0,0 "
    pts = []
    pts.append(Point(-side_length + x, 0 + y))
    pts.append(Point(-side_length * cos(pi / 3) + x, side_length * sin(pi / 3) + y))
    pts.append(Point(side_length * cos(pi / 3) + x, side_length * sin(pi / 3) + y))
    pts.append(Point(side_length + x, 0 + y))
    pts.append(Point(side_length * cos(pi / 3) + x, -side_length * sin(pi / 3) + y))
    pts.append(Point(-side_length * cos(pi / 3) + x, -side_length * sin(pi / 3) + y))
    hexagon = Polygon(pts)
    hexagon.setOutline("blue")
    hexagon.setWidth(2)
    if fill == "red":
        hexagon.setFill(color_rgb(255, 50, 50, ))
    if fill == "green":
        hexagon.setFill("green")

    return hexagon


def simulate_hex(rows, columns, path1, path2=None, side_length: int = 40, win=None, open_until_close=False,
                 slow_down: float = 0.2):
    """
        This function renders the paths of 2 agents in a hex grid
        Agent1 = grey circle with  green path
        Agent2 = black circle with blue path
        red tile = both agents have been at that location
        ####NOTE: currently only supports when the paths are of equal length####

        :param rows: number of rows in grid
        :param columns: number of columns in grid
        :param path1: path of first agent can either be a list of coordinate tuples, integers, or list pairs
        :param path2: Default None! path of second agent can either be a list of coordinate tuples, integers, or list pairs
        :param side_length: optional int side_length of the hex grid (default 40)
        :param win: optional window (default None will create window with grid lines)
        :param open_until_close: optional boolean(default False will close when all code has run) - True will stay open until click
        :param slow_down: optional float (default is 0.2 will slow down the animation by 0.2 seconds every time step)
        :return: window
        """

    # determines the size of the grids on the screen and the whitespace for the color tiles, also sets the white border
    buffer = 5
    edge_width = side_length
    half_hex_height = sqrt((side_length ** 2) - ((side_length / 2) ** 2))

    win_width = 2 * edge_width + (3 / 2) * side_length * columns - edge_width / 2
    win_height = 2 * edge_width + 2 * half_hex_height * (rows - 1)

    # initializes the agents off screen to be animated

    circle1 = Circle(Point(-10, -10), side_length / 5)
    circle2 = Circle(Point(-10, -10), side_length / 5)

    # initializes rectangle area
    rect = Rectangle(Point(edge_width, edge_width), Point(win_width - edge_width, win_height - edge_width))

    # Creates new graphics window if none given and draws the grid
    if win is None:
        win = GraphWin('HexWorld', win_width, win_height)

        # draws black grid

        for i in range(rows):
            for j in range(columns):

                if j % 2 == 0 and i != (rows - 1):  # adds short columns (even)

                    x = edge_width + (side_length / 2) + 1.5 * side_length * j
                    y = edge_width + half_hex_height + 2 * half_hex_height * i

                    hex = hexagon(x=x, y=y, side_length=side_length)
                    hex.draw(win)


                elif j % 2 == 1:  # adds long columns (odd)

                    x = edge_width + (side_length / 2) + 1.5 * side_length * j
                    y = edge_width + 2 * half_hex_height * i

                    hex = hexagon(x=x, y=y, side_length=side_length)
                    hex.draw(win)

    path_length = len(path1)

    # goes through each point in the paths of both agents and performs each action
    # NOTE: currently only supports when the paths are of equal length #

    for i in range(path_length):
        time.sleep(slow_down)
        agent1 = path1[i]
        if path2 is not None:
            agent2 = path2[i]

        num_visits_1 = int(path1[0:i + 1].count(agent1))
        if path2 is not None:
            num_visits_1 = int(path1[0:i + 1].count(agent1) + path2[0:i + 1].count(agent1))
            num_visits_2 = int(path1[0:i + 1].count(agent2) + path2[0:i + 1].count(agent2))

        if type(path1[i]) is tuple or type(path1[i]) is list:
            agent1 = tuple_to_single_index(path1[i], columns)

        if path2 is not None:
            if type(path2[i]) is tuple or type(path2[i]) is list:
                agent2 = tuple_to_single_index(path2[i], columns)

        coord1 = num_to_coord(agent1, columns)
        if path2 is not None:
            coord2 = num_to_coord(agent2, columns)

        # initializes x,y coord in case no assignment ( None type error instead of ref before assign)
        x_1, x_2, y_1, y_2 = None, None, None, None

        if coord1[1] % 2 == 0 and coord1[0] != (rows - 1):  # short columns (even)

            x_1 = edge_width + (side_length / 2) + 1.5 * side_length * coord1[1]
            y_1 = edge_width + half_hex_height + 2 * half_hex_height * coord1[0]

        if coord1[1] % 2 == 1:  # long columns (odd)

            x_1 = edge_width + (side_length / 2) + 1.5 * side_length * coord1[1]
            y_1 = edge_width + 2 * half_hex_height * coord1[0]

        if path2 is not None:
            if coord2[1] % 2 == 0 and coord2[0] != (rows - 1):  # short columns (even)

                x_2 = edge_width + (side_length / 2) + 1.5 * side_length * coord2[1]
                y_2 = edge_width + half_hex_height + 2 * half_hex_height * coord2[0]

        if path2 is not None:
            if coord2[1] % 2 == 1:  # long columns (odd)

                x_2 = edge_width + (side_length / 2) + 1.5 * side_length * coord2[1]
                y_2 = edge_width + 2 * half_hex_height * coord2[0]

        circle1.undraw()
        if path2 is not None:
            circle2.undraw()

        circle1 = Circle(Point(x_1, y_1), side_length / 5)
        if path2 is not None:
            circle2 = Circle(Point(x_2, y_2), side_length / 5)
        circle1.setFill('grey')
        if path2 is not None:
            circle2.setFill('black')

        hex1 = hexagon(x=x_1, y=y_1, side_length=side_length - buffer)
        if path2 is not None:
            hex2 = hexagon(x=x_2, y=y_2, side_length=side_length - buffer)

        hex1.setWidth(0)
        if path2 is not None:
            hex2.setWidth(0)

        if num_visits_1 == 1:
            hex1.setFill("lightgreen")
        elif num_visits_1 > 1:
            hex1.setFill("red")

        if path2 is not None:
            if num_visits_2 == 1:
                hex2.setFill("lightblue")
            elif num_visits_2 > 1:
                hex2.setFill("red")

        hex1.draw(win)
        if path2 is not None:
            hex2.draw(win)
        circle1.draw(win)
        if path2 is not None:
            circle2.draw(win)

    # draws rectangle area
    rect.draw(win)

    if open_until_close:
        if win is not None:
            win.getMouse()
            win = None

    return win


if __name__ == '__main__':
    # hex example simulation
    # path1 = [0, 5, 11, 5, 6, 1, 2, 7, 2, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
    # path2 = [19, 14, 9, 13, 8, 8, 13, 7, 11, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16]
    #
    # simulate_hex(path1=path1, path2=path2, rows=5, columns=5, side_length=40, win=None, open_until_close=True,
    # slow_down=0.1)

    # # yin/yang square example simulation
    # path1 = [0, 1, 2, 3, 7, 6]
    # path2 = [11, 10, 9, 8, 4, 5]
    # simulate_grid(path1=path1, path2=path2, rows=3, columns=4, win=None, open_until_close=False,slow_down=0.1)
    #
    # # square example using charles' code from dual_agent_test.py
    # (path1, path2), graph = gw3x4_dual()

    # simulate_grid(graph.rows, graph.columns, path1, path2,side_length= 10,open_until_close=True,slow_down=0.4)
    #
    # ## aaron hex code example
    # rows = 3
    # cols = 3
    # agents = DoubleHexagonAgent(rows, cols)
    # agents.reset_all()
    # steps = agents.train(rounds=2500)
    # final_steps = steps[len(steps)-1]
    # path1, path2 = agents.show_paths(final_steps)
    #
    # simulate_hex(path1=path1, path2=path2, rows=int(rows), columns=int(cols), side_length=40, win=None,
    #              slow_down=0.5)
    # single agent example
    # path1 = [0, 4, 3, 7, 5, 2, 1]
    #
    # simulate_hex(path1=path1, rows=3, columns=3, side_length=40, win=None,
    #              open_until_close=True,
    #              slow_down=0.5)
    #  square example simulation
    # path1 = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 91, 92, 93, 94, 95, 96, 97, 98, 88, 78, 68, 58, 48, 38, 28, 18, 17,
    #          16, 15, 25, 35, 45, 55, 65, 75, 85, 86, 87, 77, 67, 57, 47, 37, 27, 26, 36, 46, 56, 66, 76]
    # path2 = [99, 89, 79, 69, 59, 49, 39, 29, 19, 9, 8, 7, 6, 5, 4, 3, 2, 1, 11, 21, 31, 41, 51, 61, 71, 81, 82, 83, 84,
    #          74, 64, 54, 44, 34, 24, 14, 13, 12, 22, 32, 42, 52, 62, 72, 73, 63, 53, 43, 33, 23]

    path1 = [0, 6, 7, 6, 12, 18, 19, 20, 21, 15, 16, 10, 4, 3, 2, 1, 2, 8, 14, 8, 2]
    path2 = [29, 28, 27, 26, 27, 26, 25, 24, 25, 19, 13, 14, 8, 9, 10, 4, 5, 11, 17, 23, 22]
    print(len(path1), len(path2))
    simulate_grid(path1=path1, path2=path2, rows=5, columns=6, win=None, open_until_close=True, slow_down=0.1)
