
# Eight Puzzle Solver – Heuristics and A* Search

## Problem Definition
The Eight Puzzle is a 3x3 sliding tile puzzle with eight numbered tiles and one empty space. The objective is to reach a specified goal configuration from a given initial state by sliding tiles into the empty space, using the fewest moves possible. This part explores the use of heuristic evaluation functions and the A* search algorithm to efficiently solve the puzzle, comparing the effectiveness of different heuristics in guiding the search process.

This project extends the Eight Puzzle solver with heuristic evaluation functions and the A* search algorithm. It enables comparison of heuristic strategies and demonstrates the power of informed search for solving the sliding tile puzzle efficiently.

## Features
- **Heuristic Functions:** Supports multiple heuristics (e.g., misplaced tiles, Manhattan distance) for evaluating puzzle states.
- **A* Search:** Implements the A* algorithm with selectable heuristics for optimal and efficient solutions.
- **Node Limit Option:** Restrict the maximum number of nodes generated during search to test algorithm efficiency and edge cases.
- **Randomized Scrambling:** Scramble the puzzle state with a configurable random seed for reproducible experiments.
- **Detailed Output:** Reports nodes created, solution length, and move sequence for each search.
- **Interactive and Batch Modes:** Run commands interactively or from a test file.

## Commands
The following commands are supported:

- **setState x1 x2 x3 x4 x5 x6 x7 x8 x9**
  - Sets the puzzle to a specific state, where x1 to x9 are the tile values (0 represents the empty space).
- **scrambleState n**
  - Scrambles the puzzle by making `n` random moves from the goal state.
- **setSeed n**
  - Sets the random seed for reproducible scrambling.
- **move direction**
  - Moves the empty space in the specified direction. Valid directions: `up`, `down`, `left`, `right`.
- **printState**
  - Prints the current state of the puzzle.
- **heuristic h1|h2**
  - Evaluates the current state using the specified heuristic (e.g., `h1` for misplaced tiles, `h2` for Manhattan distance).
- **solve A* h1|h2 [maxnodes=N]**
  - Solves the puzzle using A* search with the selected heuristic. Optionally limit the number of nodes generated with `maxnodes`.

Commands can be entered interactively or provided in a test file (e.g., `testcmds.txt`).

## Usage

### Running with a Test File
To execute the solver with a test file (e.g., `testcmds.txt`), run:

```bash
python3 EightPuzzle.py testcmds.txt
```

The output will be shown in the terminal and written to `output.txt`.

### Interactive Usage
You can also use the solver interactively in a Python shell:

```python
python3
import sys
sys.path.append("/path/to/downloaded/code")
from EightPuzzle import PuzzState
puzzle = PuzzState()
puzzle.cmd("setState 0 1 2 3 4 5 6 7 8")
puzzle.cmd("printState")
puzzle.cmd("heuristic h1")
puzzle.cmd("heuristic h2")
puzzle.cmd("scrambleState 5")
puzzle.cmd("heuristic h1")
puzzle.cmd("heuristic h2")
puzzle.cmd("solve A* h1 maxnodes=10000")
puzzle.cmd("solve A* h2")
```

Replace `/path/to/downloaded/code` with the actual path to the project directory.

## Example Output
```
Nodes created during search: 12
Solution length: 6
Move sequence: 
move left
move up
move right
move down
move left
move left
```

## Applications
- Demonstrates and compares heuristic search strategies.
- Useful for benchmarking and educational purposes.
- Can be extended with additional heuristics or search algorithms.

## Extensibility
- Modular design for easy integration of new algorithms or features.
- Well-documented codebase for maintainability and further development.

## Contact
For questions or collaboration opportunities, please reach out via GitHub.
