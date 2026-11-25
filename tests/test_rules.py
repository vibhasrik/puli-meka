from state import Piece, State, Move, start
from rules import legal_moves, apply_move, winner


def make(tigers=(), goats=(), to_place=0, turn=Piece.TIGER, since=0, captured=0):
    b = [Piece.EMPTY] * 23
    for p in tigers:
        b[p] = Piece.TIGER
    for p in goats:
        b[p] = Piece.GOAT
    return State(tuple(b), to_place, captured, turn, since)


def test_goats_can_place_on_any_empty_point():
    assert len(legal_moves(start((2, 5)))) == 20


def test_tiger_steps_and_jumps():
    s = apply_move(start((2, 5)), Move(dst=8))
    moves = legal_moves(s)
    assert Move(dst=14, src=2, over=8) in moves   # jump the goat
    assert Move(dst=8, src=2) not in moves         # 8 is taken
    assert len(moves) == 8                         # 7 steps + 1 jump


def test_tigers_cannot_jump_tigers():
    s = make(tigers=(0, 2))
    assert Move(dst=8, src=0, over=2) not in legal_moves(s)


def test_placement():
    s0 = start((2, 5))
    s1 = apply_move(s0, Move(dst=8))
    assert s1.board[8] == Piece.GOAT
    assert s1.goats_to_place == 14
    assert s1.turn == Piece.TIGER
    assert s0.board[8] == Piece.EMPTY  # old state untouched


def test_jump_captures_and_resets_counter():
    s = make(tigers=(2,), goats=(8, 22), since=7)
    s = apply_move(s, Move(dst=14, src=2, over=8))
    assert s.board[2] == Piece.EMPTY and s.board[8] == Piece.EMPTY
    assert s.board[14] == Piece.TIGER
    assert s.goats_captured == 1
    assert s.moves_since_capture == 0


def test_counter_only_runs_after_placement():
    during = make(tigers=(0,), goats=(19,), to_place=3)
    after = make(tigers=(0,), goats=(19,), since=5)
    assert apply_move(during, Move(dst=2, src=0)).moves_since_capture == 0
    assert apply_move(after, Move(dst=2, src=0)).moves_since_capture == 6


def test_goat_steps_after_placement():
    s = make(tigers=(0,), goats=(1,), turn=Piece.GOAT)
    assert set(legal_moves(s)) == {Move(dst=2, src=1), Move(dst=7, src=1)}


def test_stuck_goats_skip_their_turn():
    # Goat on 1 is boxed in by tigers on 2 and 7.
    s = make(tigers=(2, 7, 20), goats=(1,))
    s = apply_move(s, Move(dst=21, src=20))
    assert s.turn == Piece.TIGER


def test_no_winner_at_start():
    assert winner(start((2, 5))) is None


def test_tigers_win_by_capturing_all():
    assert winner(make(tigers=(0,), captured=15)) == Piece.TIGER


def test_goats_win_after_20_quiet_tiger_moves():
    assert winner(make(tigers=(0,), goats=(19,), since=20)) == Piece.GOAT


def test_goats_win_by_trapping():
    # Tiger on 1: neighbors 2 and 7 are goats, and 3 and 13 block the jumps.
    assert winner(make(tigers=(1,), goats=(2, 7, 3, 13))) == Piece.GOAT
