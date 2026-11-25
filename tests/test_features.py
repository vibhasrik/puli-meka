from state import Piece, start
from features import features, NAMES
from test_rules import make


def f(s):
    return dict(zip(NAMES, features(s)))


def test_one_value_per_name():
    assert len(features(start((2, 5)))) == len(NAMES)


def test_start_position():
    # Tigers on 0, 2, 5 have 8 steps: 0->3,4  2->1,3,8  5->4,6,11
    assert f(start((2, 5))) == {
        "captures": 0, "threats": 0, "tiger_mobility": 8 / 12, "clock": 0,
        "trapped_tigers": 0, "goats_to_place": 1, "tiger_turn": 0,
    }


def test_threats():
    assert f(make(tigers=(2,), goats=(8, 22)))["threats"] == 1 / 4


def test_trapped_tiger():
    x = f(make(tigers=(1, 19), goats=(2, 7, 3, 13)))
    assert x["trapped_tigers"] == 1 / 3   # 1 is boxed in, 19 is free
    assert x["tiger_mobility"] == 2 / 12  # 19 -> 14, 20


def test_counters_and_turn():
    x = f(make(tigers=(0,), captured=3, since=25, to_place=0, turn=Piece.TIGER))
    assert x["captures"] == 0.5
    assert x["clock"] == 0.5
    assert x["goats_to_place"] == 0
    assert x["tiger_turn"] == 1
