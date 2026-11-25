# Plan

| #   | Step                            | What it means                                                                  |
| --- | ------------------------------- | ------------------------------------------------------------------------------ |
| 1   | Build the game engine           | Board, state, legal moves, apply move, game over. Tested.                      |
| 2   | Make baseline opponents         | Random, greedy, and hand-tuned minimax.                                        |
| 3   | Choose features                 | A few numbers that describe a position, like goats captured or tiger mobility. |
| 4   | Define rewards                  | Win and loss values for each side.                                             |
| 5   | Self-play with TD learning      | The agent plays itself and adjusts its feature weights.                        |
| 6   | Plug learned values into search | Swap the hand-written evaluation for the learned one in minimax.               |
| 7   | Evaluate                        | Learned vs. hand-tuned win rates, learning curves, which side is favored.      |
| 8   | Stretch: neural net + MCTS      | AlphaZero-style. Only if 1 to 7 are solid.                                     |
| 9   | Package it                      | README with charts, playable demo.                                             |

## Step 1 files

1. `board.py`: `LINES`, neighbors, jumps
2. `state.py`: `State`, `Move`, starting position
3. `rules.py`: legal moves, apply move, game over
4. `tests/`: one test file per file above
