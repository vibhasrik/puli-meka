from board import LINES, NEIGHBORS, JUMPS


def test_every_point_is_on_some_line():
    assert {p for line in LINES for p in line} == set(range(23))


def test_neighbors_of_a_few_points():
    assert NEIGHBORS[0] == {2, 3, 4, 5}
    assert NEIGHBORS[2] == {0, 1, 3, 8}
    assert NEIGHBORS[1] == {2, 7}
    assert NEIGHBORS[19] == {14, 20}


def test_neighbors_are_symmetric():
    for p, ns in NEIGHBORS.items():
        for q in ns:
            assert p in NEIGHBORS[q]


def test_jumps_from_apex():
    assert {j for j in JUMPS if j[0] == 0} == {(0, 2, 8), (0, 3, 9), (0, 4, 10), (0, 5, 11)}


def test_jumps_go_both_ways():
    assert (8, 2, 0) in JUMPS
    assert (13, 7, 1) in JUMPS


def test_no_jump_wraps_around_a_corner():
    # 1 -> 2 -> 8 bends from the top row onto a ray, so it is not straight.
    assert (1, 2, 8) not in JUMPS


def test_counts():
    # 38 edges between neighbors, 56 directed jumps.
    assert sum(len(ns) for ns in NEIGHBORS.values()) == 2 * 38
    assert len(JUMPS) == 56
