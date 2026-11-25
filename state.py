from enum import Enum
from dataclasses import dataclass

class Piece(Enum):
    EMPTY = 1
    GOAT = 2
    TIGER = 3

@dataclass(frozen=True)
class State:
    board: tuple
    goats_to_place: int
    goats_captured: int
    turn: Piece
    moves_since_capture: int

@dataclass(frozen=True)
class Move:
    dst: int
    src: int | None = None
    over: int = None

def start(tigers) -> State:
    if len(set(tigers)) != 2:
      raise ValueError("Invalid tiger positions: must be only 2")
    b=[Piece.EMPTY,] * 23  # need to add tiger at the apex
    b[0] = Piece.TIGER
    for p in tigers:
      if not (2 <= p <= 5):
        raise ValueError("Invalid tiger position: must be between 2 and 5")
      b[p] = Piece.TIGER

    return State(
      board=tuple(b),
      goats_to_place=15,
      goats_captured=0,
      turn=Piece.GOAT,
      moves_since_capture=0
    )