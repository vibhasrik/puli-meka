# Rules

## Setup

- 1 tiger starts on the apex (point 0).
- 2 tigers start on any of points 2, 3, 4, 5. The tiger player picks the two points before the game starts.
- 15 goats start off the board.

## Turns

Goats go first. Players alternate.

|                               | Goats                             | Tigers                             |
| ----------------------------- | --------------------------------- | ---------------------------------- |
| While goats are left to place | Place one goat on any empty point | Step to an empty neighbor, or jump |
| After all 15 are placed       | Step to an empty neighbor         | Same                               |

## Jumping

- A tiger jumps over **one** goat to the empty point right behind it.
- The jump must go in a straight line.
- The jumped goat is captured.
- Tigers can't jump tigers. Goats never jump.
- Capturing is optional. A tiger may skip a capture that would get it trapped.

## Winning

- **Tigers:** capture 6 goats. (Sources differ: 5, 6, or all 15. I picked 6.)
- **Goats:** leave no tiger with a legal move.

## Edge cases

| Case                                                                                 | Rule                            |
| ------------------------------------------------------------------------------------ | ------------------------------- |
| Tigers go 50 moves in a row without a capture, counted after all 15 goats are placed | Goats win (tigers are cornered) |
| A goat's turn, but no goat can move                                                  | Goats skip their turn           |
