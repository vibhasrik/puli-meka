import pytest

from state import Piece, State, Move, start


def test_start_board():
    s = start(tigers=(2, 5))
    assert isinstance(s.board, tuple)
    assert len(s.board) == 23
    tigers = {p for p, piece in enumerate(s.board) if piece == Piece.TIGER}
    assert tigers == {0, 2, 5}
    assert Piece.GOAT not in s.board


def test_start_counters():
    s = start(tigers=(3, 4))
    assert s.goats_to_place == 15
    assert s.goats_captured == 0
    assert s.turn == Piece.GOAT
    assert s.moves_since_capture == 0


def test_tiger_order_does_not_matter():
    assert start(tigers=(2, 5)) == start(tigers=(5, 2))


@pytest.mark.parametrize("tigers", [(2, 2), (0, 2), (1, 2), (2, 8), (2,), (2, 3, 4)])
def test_bad_tiger_points_are_rejected(tigers):
    with pytest.raises(ValueError):
        start(tigers=tigers)


def test_state_cannot_be_changed():
    s = start(tigers=(2, 5))
    with pytest.raises(AttributeError):
        s.goats_to_place = 0


def test_state_works_as_dict_key():
    seen = {start(tigers=(2, 5)): "score"}
    assert seen[start(tigers=(2, 5))] == "score"


def test_moves():
    place = Move(dst=8)
    step = Move(dst=8, src=2)
    jump = Move(dst=14, src=2, over=8)
    assert place.src is None and place.over is None
    assert step.over is None
    assert jump == Move(dst=14, src=2, over=8)
    assert len({place, step, jump}) == 3  # Moves are hashable too
