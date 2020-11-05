
def single_index_to_tuple(index, cols):
    """
    Turns a single index of our hexagonal tesselation (from a graph) into a tuple (i,j) pair.
    ( the harder logic version w/o the missing invisible entires in on my points_to_gps.py file
    :param index: single index
    :return: tuple
    """
    i = index // cols
    j = index % cols
    return i, j


def tuple_to_single_index(tuple, cols):
    """
    Turns a tuple (i,j) pair of our hexagonal tesselation into a single index (from a graph).
    :param tuple:
    :return: single index
    """
    return tuple[0]*cols + tuple[1]


def nums_to_ops(nums, rows, cols):
    """
    Turns a path based off a single-index from something like
       1     3      5
    0     2     4
       7     9     11
    6     8    10
       12    13     14
    to a list of ordered pairs that is compatible with my path_to_coords() function
    WARNING!!! THIS IS OLD/ depreacted
    :param nums: numbers
    :param rows: rows in hexagon graph
    :param cols: columns in hexagon graph
    :return: a list of ordered pairs
    """
    op_path = []

    for num in nums:
        i = num//cols
        j = num % cols
        if i == rows - 1:  # if its in the last row
            last_reg = (rows-1)*cols - 1  # last regular ( from the last full row)
            diff = num - last_reg  # finds how much further our num is from the last number
            j = 2*diff - 1  # declares what the new column is ( it does by twos now!.\
        op_path.append([i, j])
    return op_path


# idk if these will work
def optimal_action_q(q_table, state, rows, cols):
    """optimal action for a specified q table"""
    max_value = -10000
    action = ""
    possible_actions = find_moves_hexagons(state, rows, cols)
    for a in possible_actions:
        next_value = q_table[tuple(state)][a]
        if next_value >= max_value:
            action = a
            max_value = next_value
    return action


def show_path(indv_q_table, rows, cols):
    """show path defined for this special double agent"""
    # env = HexagonEnv()
    direction_dict = {'up': 1,
                      'up_right': 2,
                      'down_right': 3,
                      'down': 4,
                      'down_left': 5,
                      'up_left': 6}

    for i in range(rows):
        row_string = ""
        for j in range(cols):
            state = (i, j)
            best_move = optimal_action_q(indv_q_table, state, rows, cols)
            if i != rows - 1 or j % 2 == 1:
                row_string = row_string + " " + str(direction_dict[best_move])
            else:
                row_string = row_string + "  "
        print(row_string)
