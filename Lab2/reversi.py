import random
import time

CLEAR, EDGE, BLACK, WHITE = ".", "-", "B", "W"
PLAYERS = {BLACK: 'Black', WHITE: 'White'}
UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)


def all_valid_spaces():
    """List all the valid squares on the board."""
    return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]


def initial_board():
    board = [EDGE] * 100
    for i in all_valid_spaces():
        board[i] = CLEAR

    board[44], board[45] = WHITE, BLACK
    board[54], board[55] = BLACK, WHITE
    return board


def print_board(board):
    rep = ''
    rep += '  %s\n' % ' '.join(map(str, range(1, 9)))
    for row in range(1, 9):
        begin, end = 10 * row + 1, 10 * row + 9
        rep += '%d %s\n' % (row, ' '.join(board[begin:end]))
    return rep


def valid_move(move):
    if isinstance(move, int) and move in all_valid_spaces():
        return True
    return False


def opponent(player):
    if player is WHITE:
        return BLACK
    else:
        return WHITE


def enclosing_area_of_a_piece(square, player, board, direction):
    bracket = square + direction
    if board[bracket] == player:
        return None
    opp = opponent(player)
    while board[bracket] == opp:
        bracket += direction
    return None if board[bracket] in (EDGE, CLEAR) else bracket


def is_legal_move(move, player, board):
    hasbracket = lambda direction: enclosing_area_of_a_piece(move, player, board, direction)
    return board[move] == CLEAR and any(map(hasbracket, DIRECTIONS))


def make_move(move, player, board):
    """Update the board to reflect the move by the specified player."""
    board[move] = player
    for d in DIRECTIONS:
        make_flips(move, player, board, d)
    return board


def make_flips(move, player, board, direction):
    """Flip pieces in the given direction as a result of the move by player."""
    bracket = enclosing_area_of_a_piece(move, player, board, direction)
    if not bracket:
        return
    square = move + direction
    while square != bracket:
        board[square] = player
        square += direction


class IllegalMoveError(Exception):
    def __init__(self, player, move, board):
        self.player = player
        self.move = move
        self.board = board

    def __str__(self):
        return '%s cannot move to square %d' % (PLAYERS[self.player], self.move)


def legal_moves(player, board):
    """Get a list of all legal moves for player."""
    return [sq for sq in all_valid_spaces() if is_legal_move(sq, player, board)]


def any_legal_move(player, board):
    """Can player make any moves?"""
    return any(is_legal_move(sq, player, board) for sq in all_valid_spaces())


def play(black_strategy, white_strategy):
    """Play a game of Othello and return the final board and score."""
    board = initial_board()
    player = WHITE
    total_time = 0
    count = 0
    strategy = lambda who: white_strategy if who == WHITE else black_strategy
    while player is not None:
        start_time2 = time.time()
        move = get_move(strategy(player), player, board)
        make_move(move, player, board)
        total_time += (time.time() - start_time2)
        # print("time to make  a single move ", count , " : ", start_time2 - time.time())
        count += 1
        player = next_player(board, player)
    print("average_t to make a single move", total_time / count)
    return board, score(WHITE, board)


def next_player(board, prev_player):
    """Which player should move next?  Returns None if no legal moves exist."""
    opp = opponent(prev_player)
    if any_legal_move(opp, board):
        return opp
    elif any_legal_move(prev_player, board):
        return prev_player
    return None


def get_move(strategy, player, board):
    """Call strategy(player, board) to get a move."""
    copy = list(board)  # copy the board to prevent cheating
    move = strategy(player, copy)
    if not valid_move(move) or not is_legal_move(move, player, board):
        raise IllegalMoveError(player, move, copy)
    return move


def score(player, board):
    """Compute player's score (number of player's pieces minus opponent's)."""
    mine, theirs = 0, 0
    opp = opponent(player)
    for sq in all_valid_spaces():
        piece = board[sq]
        if piece == player:
            mine += 1
        elif piece == opp:
            theirs += 1
    return mine - theirs


def random_strategy(player, board):
    """A strategy that always chooses a random legal move."""
    return random.choice(legal_moves(player, board))


SQUARE_WEIGHTS = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 120, -20, 20, 5, 5, 20, -20, 120, 0,
    0, -20, -40, -5, -5, -5, -5, -40, -20, 0,
    0, 20, -5, 15, 3, 3, 15, -5, 20, 0,
    0, 5, -5, 3, 3, 3, 3, -5, 5, 0,
    0, 5, -5, 3, 3, 3, 3, -5, 5, 0,
    0, 20, -5, 15, 3, 3, 15, -5, 20, 0,
    0, -20, -40, -5, -5, -5, -5, -40, -20, 0,
    0, 120, -20, 20, 5, 5, 20, -20, 120, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]


# A strategy constructed as `maximizer(weighted_score)`, then, will always
# return the move that results in the largest immediate *weighted* gain in
# pieces.

def weighted_score(player, board):
    """
    Compute the difference between the sum of the weights of player's
    squares and the sum of the weights of opponent's squares.
    """
    opp = opponent(player)
    total = 0
    for sq in all_valid_spaces():
        if board[sq] == player:
            total += SQUARE_WEIGHTS[sq]
        elif board[sq] == opp:
            total -= SQUARE_WEIGHTS[sq]
    return total


def f_weighted_score_randomised(player, board):
    opp = opponent(player)
    total = 0
    for sq in all_valid_spaces():
        if board[sq] == player:
            total += SQUARE_WEIGHTS[sq]
        elif board[sq] == opp:
            total -= SQUARE_WEIGHTS[sq]
    return total + random.randint(-40, 40)


# <a id="minimax"></a>
### Minimax search


def minimax(player, board, depth, evaluate):
    """
    Find the best legal move for player, searching to the specified depth.
    Returns a tuple (move, min_score), where min_score is the guaranteed minimum
    score achievable for player if the move is made.
    """

    def value(board):
        return -minimax(opponent(player), board, depth - 1, evaluate)[0]

    if depth == 0:
        return evaluate(player, board), None

    moves = legal_moves(player, board)

    if not moves:

        if not any_legal_move(opponent(player), board):
            return final_value(player, board), None

        return value(board), None

    return max((value(make_move(m, player, list(board))), m) for m in moves)


accesses = []


def evaluate(player, board):
    accesses.append(player)
    return weighted_score(player, board)
    # return score(player, board)


# Values for endgame boards are big constants.
MAX_VALUE = sum(map(abs, SQUARE_WEIGHTS))
MIN_VALUE = -MAX_VALUE


def final_value(player, board):
    """The game is over--find the value of this board to player."""
    diff = score(player, board)
    if diff < 0:
        return MIN_VALUE
    elif diff > 0:
        return MAX_VALUE
    return diff


def minimax_searcher(depth, evaluate):
    def strategy(player, board):
        return minimax(player, board, depth, evaluate)[1]

    return strategy


def alphabeta(player, board, alpha, beta, depth, evaluate):
    """
    Find the best legal move for player, searching to the specified depth.  Like
    minimax, but uses the bounds alpha and beta to prune branches.
    """
    if depth == 0:
        return evaluate(player, board), None

    def value(board, alpha, beta):
        # Like in `minimax`, the value of a board is the opposite of its value
        # to the opponent.  We pass in `-beta` and `-alpha` as the alpha and
        # beta values, respectively, for the opponent, since `alpha` represents
        # the best score we know we can achieve and is therefore the worst score
        # achievable by the opponent.  Similarly, `beta` is the worst score that
        # our opponent can hold us to, so it is the best score that they can
        # achieve.
        return -alphabeta(opponent(player), board, -beta, -alpha, depth - 1, evaluate)[0]

    moves = legal_moves(player, board)
    if not moves:
        if not any_legal_move(opponent(player), board):
            return final_value(player, board), None
        return value(board, alpha, beta), None

    best_move = moves[0]
    for move in moves:
        if alpha >= beta:
            break
        val = value(make_move(move, player, list(board)), alpha, beta)
        if val > alpha:
            alpha = val
            best_move = move
    return alpha, best_move


def alphabeta_searcher(depth, evaluate):
    def strategy(player, board):
        return alphabeta(player, board, MIN_VALUE, MAX_VALUE, depth, evaluate)[1]

    return strategy

    # board = initial_board()
    # print(print_board(board))
