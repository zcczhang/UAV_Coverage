
def find_moves_squares(state, BOARD_ROWS, BOARD_COLS):  # state is a tuple
    moves = {'up', 'down', 'left', 'right'}
    if state[0] == 0:
        moves.remove('up')
    if state[0] == BOARD_ROWS - 1:
        moves.remove('down')
    if state[1] == 0:
        moves.remove('left')
    if state[1] == BOARD_COLS - 1:
        moves.remove('right')
    return list(moves)


def find_moves_hexagons(state, BOARD_ROWS, BOARD_COLS):  # state is a tuple
    # with hexagons, BOARD_ROWS refers to the most amount of
    moves = {'up', 'down', 'up_left', 'up_right', 'down_left', 'down_right'}
    if state[0] == 0:
        moves.discard('up')
        if state[1] % 2 == 1:
            moves.discard('up_left')
            moves.discard('up_right')
    if state[0] == BOARD_ROWS - 2 and state[1] % 2 == 0:
        moves.discard('down')
    if state[0] == BOARD_ROWS - 1:
        moves.discard('down')
        moves.discard('down_left')
        moves.discard('down_right')
    if state[1] == 0:
        moves.discard('up_left')
        moves.discard('down_left')
    if state[1] == BOARD_COLS - 1:
        moves.discard('up_right')
        moves.discard('down_right')
    if state[1] == BOARD_COLS - 2 and state[1] % 2 == 0:  # bottom of a shorter column
        moves.discard('down')
    return list(moves)
