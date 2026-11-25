# Design

## The board is a list of lines

A jump has to stay on a straight line, so the line is what I model.

```python
LINES = [
    [0, 2, 8, 14, 19], [0, 3, 9, 15, 20],   # rays from the apex
    [0, 4, 10, 16, 21], [0, 5, 11, 17, 22],
    [1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12],  # rows
    [13, 14, 15, 16, 17, 18], [19, 20, 21, 22],
    [1, 7, 13], [6, 12, 18],                    # sides
]
```

From this one list the code builds:

- **Neighbors**: any two points next to each other on a line.
- **Jumps**: any three points in a row on a line, in both directions.

**What I didn't do:** store (x, y) positions and check that a jump is straight with geometry. That works too, but it adds floating-point math to something that's really just "which points are in a row."

## State is small and can't be changed

A game state holds only what's needed to continue:

- what's on each point
- goats left to place
- goats captured
- whose turn it is
- tiger moves since the last capture (counted only after all goats are placed)

Everything else, like legal moves, is computed from it. A move returns a new state instead of changing the old one, which keeps search safe and lets states be used as dictionary keys.
