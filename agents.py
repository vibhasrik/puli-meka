import math
import random
from dataclasses import replace

from state import Piece, start
from rules import legal_moves, apply_move, winner

WIN = 1000
CLOCK_WEIGHT = 0.5  # points tigers lose per quiet move

# evaluates cur state (s) for tiger; higher = better for tiger
def evaluate(s):
    w = winner(s)
    if w == Piece.TIGER:
        return WIN
    if w == Piece.GOAT:
        return -WIN
    tiger_moves = legal_moves(replace(s, turn=Piece.TIGER))
    threats = sum(m.over is not None for m in tiger_moves)
    return (10 * s.goats_captured + 2 * threats + len(tiger_moves)
            - CLOCK_WEIGHT * s.moves_since_capture)

# chooses random legal moves for cur turn
def random_agent(s):
    return random.choice(legal_moves(s))

# chooses move w best score 1 move ahead; random tiebreak
def greedy_agent(s):
    sign = 1 if s.turn == Piece.TIGER else -1
    return max(legal_moves(s),
               key=lambda m: (sign * evaluate(apply_move(s, m)), random.random()))

# returns best possible score from this state by minimax search to depth
# doesn't go down any path that's pruned by alpha-beta
# assumes both sides play their best
def minimax(s, depth, alpha=-math.inf, beta=math.inf):
    if depth == 0 or winner(s) is not None:
        return evaluate(s)
    tiger = s.turn == Piece.TIGER
    best = -math.inf if tiger else math.inf
    for m in sorted(legal_moves(s), key=lambda m: m.over is None):
        score = minimax(apply_move(s, m), depth - 1, alpha, beta)
        if tiger:
            best = max(best, score)
            alpha = max(alpha, best)
        else:
            best = min(best, score)
            beta = min(beta, best)
        if alpha >= beta:
            break
    return best

# same as greedy but uses minimax instead of evaluate to choose next move
def minimax_agent(s, depth=3):
    sign = 1 if s.turn == Piece.TIGER else -1
    return max(legal_moves(s),
               key=lambda m: (sign * minimax(apply_move(s, m), depth - 1), random.random()))


# simulates a game
def play(tiger, goat, tigers=(2, 5)):
    s = start(tigers)
    while (w := winner(s)) is None:
        agent = tiger if s.turn == Piece.TIGER else goat
        s = apply_move(s, agent(s))
    return w
