import random

from state import Piece, Move, start
from rules import legal_moves, apply_move, winner
from agents import random_agent, greedy_agent, play, minimax, minimax_agent, evaluate, WIN
from test_rules import make


def test_random_agent_picks_a_legal_move():
    s = start((2, 5))
    assert random_agent(s) in legal_moves(s)


def test_greedy_tiger_takes_a_capture():
    s = make(tigers=(2,), goats=(8, 22))
    assert greedy_agent(s) == Move(dst=14, src=2, over=8)


def test_greedy_goat_does_not_hand_over_a_goat():
    s = make(tigers=(0,), to_place=5, turn=Piece.GOAT)
    after = apply_move(s, greedy_agent(s))
    assert not any(m.over is not None for m in legal_moves(after))


def test_games_finish():
    for _ in range(20):
        assert play(random_agent, random_agent) in (Piece.TIGER, Piece.GOAT)


def test_minimax_depth_zero_is_just_evaluate():
    s = start((2, 5))
    assert minimax(s, 0) == evaluate(s)


def test_minimax_sees_a_finished_game():
    assert minimax(make(tigers=(0,), captured=15), 3) == WIN


def test_minimax_tiger_takes_a_capture():
    s = make(tigers=(2,), goats=(8, 22))
    assert minimax_agent(s, depth=2) == Move(dst=14, src=2, over=8)


def test_minimax_goat_finishes_a_trap():
    # Tiger on 1 is boxed in except for point 2. Placing there wins.
    s = make(tigers=(1,), goats=(7, 3, 13), to_place=5, turn=Piece.GOAT)
    assert minimax_agent(s, depth=2) == Move(dst=2)


def plain_minimax(s, depth):
    if depth == 0 or winner(s) is not None:
        return evaluate(s)
    scores = [plain_minimax(apply_move(s, m), depth - 1) for m in legal_moves(s)]
    return max(scores) if s.turn == Piece.TIGER else min(scores)


def test_alpha_beta_matches_plain_minimax():
    rng = random.Random(0)
    for _ in range(15):
        s = start((2, 5))
        for _ in range(rng.randrange(40)):
            if winner(s) is not None:
                break
            s = apply_move(s, rng.choice(legal_moves(s)))
        assert minimax(s, 3) == plain_minimax(s, 3)
