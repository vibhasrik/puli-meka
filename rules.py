from dataclasses import replace

from board import NEIGHBORS, JUMPS
from state import Piece, State, Move

QUIET_LIMIT = 50  # tiger moves without a capture before goats win
CAPTURE_LIMIT = 6  # captures tigers need to win


def other(side):
    return Piece.TIGER if side == Piece.GOAT else Piece.GOAT


def legal_moves(s: State) -> list[Move]:
    b = s.board
    if s.turn == Piece.GOAT and s.goats_to_place:
        return [Move(dst=p) for p in range(23) if b[p] == Piece.EMPTY]
    moves = [Move(dst=q, src=p)
             for p in range(23) if b[p] == s.turn
             for q in NEIGHBORS[p] if b[q] == Piece.EMPTY]
    if s.turn == Piece.TIGER:
        moves += [Move(dst=c, src=a, over=o) for a, o, c in JUMPS
                  if b[a] == Piece.TIGER and b[o] == Piece.GOAT and b[c] == Piece.EMPTY]
    return moves


# Trusts that m came from legal_moves(s); minimax calls this a lot, so no re-check.
def apply_move(s: State, m: Move) -> State:
    b = list(s.board)
    if m.src is not None:
        b[m.src] = Piece.EMPTY
    if m.over is not None:
        b[m.over] = Piece.EMPTY
    b[m.dst] = s.turn

    to_place = s.goats_to_place - (m.src is None)
    since = s.moves_since_capture
    if s.turn == Piece.TIGER:
        # Reset on a capture. Only count once all goats are placed.
        since = 0 if m.over is not None or to_place else since + 1

    new = State(tuple(b), to_place, s.goats_captured + (m.over is not None),
                other(s.turn), since)
    if new.turn == Piece.GOAT and not legal_moves(new):
        new = replace(new, turn=Piece.TIGER)  # stuck goats skip their turn
    return new


def winner(s: State):
    """Piece.TIGER, Piece.GOAT, or None if the game isn't over."""
    if s.goats_captured >= CAPTURE_LIMIT:
        return Piece.TIGER
    if s.moves_since_capture >= QUIET_LIMIT:
        return Piece.GOAT
    if s.turn == Piece.TIGER and not legal_moves(s):
        return Piece.GOAT
    return None
