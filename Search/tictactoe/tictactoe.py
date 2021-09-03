"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_number = 0
    o_number = 0
    for row in board:
        x_number = x_number + row.count(X)
        o_number = o_number + row.count(O)
    
    if (x_number == 0 and o_number == 0) or x_number <= o_number:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    avai_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                avai_actions.add((i,j))
    if not avai_actions:
        return None
    return avai_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action is None:
        return board
    new_board = copy.deepcopy(board)
    # if not (action in actions(board)):
    #     raise Exception('Invalid action, please choose the right action!')
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if (board[i][0] == board[i][1] == board[i][2]) and board[i][0] != EMPTY:
            if board[i][0] == X:
                return X
            else:
                return O
    for i in range(3):
        if (board[0][i] == board[1][i] == board[2][i]) and board[0][i] != EMPTY:
            if board[0][i] == X:
                return X
            else:
                return O
    if (board[0][0] == board[1][1] == board[2][2]) and board[0][0] != EMPTY:
        if board[0][0] == X:
            return X
        else:
            return O
    if (board[0][2] == board[1][1] == board[2][0]) and board[0][2] != EMPTY:
        if board[0][2] == X:
            return X
        else:
            return O
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    win = winner(board)
    if win == X or win == O:
        return True
    elif actions(board) is None:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board) == True:
        win = winner(board)
        if win is X:
            return 1
        elif win is O:
            return -1
        else:
            return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) is True:
        return None
    else:
        if player(board) is X:
            if board == initial_state():
                return (1,1)
            else:
                copy_actions = copy.deepcopy(actions(board))
                best_action = copy_actions.pop()
                best_value = -math.inf
                for a in actions(board):
                    if actions(result(board, a)) is None:
                        return best_action
                    n = min_value(result(board, a))
                    if n >= best_value:
                        best_value = n
                        best_action = a
                return best_action

        if player(board) is O:
            copy_actions = copy.deepcopy(actions(board))
            best_action = copy_actions.pop()
            best_value = math.inf
            for a in actions(board):
                if actions(result(board, a)) is None:
                    return best_action
                n = max_value(result(board, a))
                if n <= best_value:
                    best_value = n
                    best_action = a
            return best_action

def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for a in actions(board):
        # if actions(result(board, a)) is None:
        #     return v
        v = max(v, min_value(result(board, a)))
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for a in actions(board):
        # if actions(board) is None:
        #     return v
        v = min(v, max_value(result(board, a)))
    return v