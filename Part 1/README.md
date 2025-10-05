
# Eight Puzzle Solver

## Problem Definition
The Eight Puzzle is a classic sliding tile puzzle consisting of a 3x3 grid with eight numbered tiles and one empty space. The objective is to transform a given initial configuration of tiles into a specified goal configuration by sliding tiles one at a time into the empty space. Only tiles adjacent to the empty space can be moved, and the challenge is to reach the goal state using the minimum number of moves possible. This problem is fundamental in the study of search algorithms and state-space exploration.

This project implements a solver for the classic Eight Puzzle problem, a sliding tile puzzle consisting of a 3x3 grid with eight numbered tiles and one empty space. The objective is to rearrange the tiles from an initial configuration to a specified goal configuration by sliding tiles into the empty space, using the minimum number of moves.

## Features
- **Configurable Initial and Goal States:** Easily set any valid starting and goal arrangement.
- **State Representation:** Efficient internal representation of puzzle states for fast computation.
- **Move Generation:** Supports all valid moves (up, down, left, right) based on the current empty space position.
- **Solution Search:** Designed to be compatible with various search algorithms (e.g., BFS, DFS, A*, etc.).
- **Traceable Output:** Outputs the sequence of moves and states leading to the solution.

## Example
Given an initial state:
```
1 2 3
4 5 6
7 8  
```
And a goal state:
```
1 2 3
4 5 6
7 8  
```
The solver finds the optimal sequence of moves to reach the goal.


## Commands

The following commands are supported by the Eight Puzzle solver:

- **setState x1 x2 x3 x4 x5 x6 x7 x8 x9**
	- Sets the puzzle to a specific state, where x1 to x9 are the tile values (0 represents the empty space).
	- Example: `setState 7 2 4 5 0 6 8 3 1`

- **scrambleState n**
	- Scrambles the puzzle by making `n` random moves from the goal state.
	- Example: `scrambleState 6`

- **move direction**
	- Moves the empty space in the specified direction. Valid directions: `up`, `down`, `left`, `right`.
	- Example: `move up`

- **printState**
	- Prints the current state of the puzzle.

Commands can be entered interactively or provided in a test file (e.g., `testcmds.txt`).

### Running with a Test File

To execute the solver with a test file (e.g., `testcmds.txt`), run:

```bash
python3 EightPuzzle.py testcmds.txt
```

The `testcmds.txt` file contains test cases and edge cases for the puzzle. The output will be written to `output.txt`.

### Interactive Usage

You can also use the solver interactively in a Python shell:

```python
python3
import sys
sys.path.append("/path/to/downloaded/code")
from EightPuzzle import PuzzState
puzzle = PuzzState()
puzzle.cmd("setState 7 2 4 5 0 6 8 3 1")
puzzle.cmd("printState")
```

Replace `/path/to/downloaded/code` with the actual path to the project directory.

## Applications
- Demonstrates problem-solving and search techniques in AI.
- Useful for benchmarking search algorithms and heuristics.
- Can be extended for larger sliding puzzles or integrated into educational tools.

## Extensibility
- Modular design allows for easy integration of new search strategies or heuristics.
- Well-documented codebase for maintainability and further development.

## Contact
For questions or collaboration opportunities, please reach out via GitHub.
