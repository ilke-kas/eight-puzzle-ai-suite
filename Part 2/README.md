
# Eight Puzzle Solver – Search Algorithms

## Problem Definition
The Eight Puzzle is a 3x3 sliding tile puzzle with eight numbered tiles and one empty space. The task is to rearrange the tiles from a given initial configuration to a specified goal configuration by sliding tiles into the empty space, one move at a time. Only tiles adjacent to the empty space can be moved. This part focuses on solving the puzzle using uninformed search algorithms, such as Depth-First Search (DFS) and Breadth-First Search (BFS), and analyzing their performance in terms of nodes generated and solution length.

This project extends the classic Eight Puzzle solver by implementing and comparing uninformed search algorithms, specifically Depth-First Search (DFS) and Breadth-First Search (BFS). The solver can be configured to use different search strategies and node limits, providing insight into algorithmic performance and efficiency.

## Features
- **DFS and BFS Solvers:** Choose between Depth-First Search and Breadth-First Search for solving the puzzle.
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
- **solve DFS [maxnodes=N]**
  - Solves the puzzle using Depth-First Search. Optionally limit the number of nodes generated with `maxnodes`.
- **solve BFS [maxnodes=N]**
  - Solves the puzzle using Breadth-First Search. Optionally limit the number of nodes generated with `maxnodes`.

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
puzzle.cmd("move right")
puzzle.cmd("printState")
puzzle.cmd("solve DFS")
puzzle.cmd("solve BFS")
```

Replace `/path/to/downloaded/code` with the actual path to the project directory.

## Example Output
```
Nodes created during search: 5
Solution length: 2
Move sequence: 
move left
move left
```

## Applications
- Demonstrates and compares uninformed search strategies.
- Useful for benchmarking and educational purposes.
- Can be extended with additional search algorithms or heuristics.

## Extensibility
- Modular design for easy integration of new algorithms or features.
- Well-documented codebase for maintainability and further development.

## Contact
For questions or collaboration opportunities, please reach out via GitHub.
