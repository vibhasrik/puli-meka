from dataclasses import replace

from state import Piece
from rules import legal_moves, CAPTURE_LIMIT, QUIET_LIMIT

NAMES = [
    "captures",
    "threats",
    "tiger_mobility",
    "clock",
    "trapped_tigers",
    "goats_to_place",
    "tiger_turn",
]


def features(s):
    tiger_moves = legal_moves(replace(s, turn=Piece.TIGER))
    threats = sum(m.over is not None for m in tiger_moves)
    movers = {m.src for m in tiger_moves}
    trapped = sum(piece == Piece.TIGER and p not in movers for p, piece in enumerate(s.board))
    return [
        s.goats_captured / CAPTURE_LIMIT,
        threats / 4,
        len(tiger_moves) / 12,
        s.moves_since_capture / QUIET_LIMIT,
        trapped / 3,
        s.goats_to_place / 15,
        1.0 if s.turn == Piece.TIGER else 0.0,
    ]
