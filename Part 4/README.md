
# Eight Puzzle Solver – Search Cost Analysis & Branching Factor

## Problem Definition
The Eight Puzzle is a 3x3 sliding tile puzzle with eight numbered tiles and one empty space. The challenge is to transform an initial configuration into a goal configuration by sliding tiles into the empty space, using the minimum number of moves. This part investigates the empirical analysis of search costs, effective branching factors, and algorithmic performance, providing tools for benchmarking and reporting on the efficiency of various search strategies applied to the puzzle.

This project extends the Eight Puzzle solver with tools for analyzing search costs, effective branching factors, and algorithmic performance. It enables empirical comparison of search strategies and provides utilities for generating and evaluating test cases, with results exportable for further analysis.

## Features
- **Effective Branching Factor Calculation:** Evaluate the effective branching factor for uniform trees of specified branching factor and height.
- **Search Cost Comparison:** Compare the performance (nodes generated, solution length) of different search algorithms on a variety of puzzle states.
- **State Generation for Benchmarking:** Generate sets of puzzle states at varying depths for systematic benchmarking.
- **Automated Table Generation:** Export results as LaTeX tables and images for reporting and visualization.
- **Interactive and Batch Modes:** Run commands interactively or from a test file.

## Commands
The following commands are supported:

- **testEBF b h**
  - Calculates the effective branching factor for a uniform tree with branching factor `b` and height `h`.
- **compareSearchCosts**
  - Compares the search costs (e.g., nodes generated, solution lengths) of different algorithms on a set of states. Results are saved as LaTeX tables and images.
- **createsStatesSearchCost d_min d_max step**
  - Generates puzzle states at depths from `d_min` to `d_max` (inclusive) in steps of `step` for benchmarking.
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
puzzle.cmd("testEBF 2 4")
puzzle.cmd("testEBF 5 5")
puzzle.cmd("testEBF 4 10")
puzzle.cmd("compareSearchCosts")
puzzle.cmd("createsStatesSearchCost 6 20 2")
puzzle.cmd("createsStatesSearchCost 5 25 5")
```

Replace `/path/to/downloaded/code` with the actual path to the project directory.

## Output & Reporting
- Results of search cost comparisons and effective branching factor calculations are saved as LaTeX tables and images (see `table_b_stars.tex`, `table_number_of_nodes_generated.tex`, `table_solution_lengths.tex`, and `Tables_for_Comparision.png`).

## Applications
- Empirical analysis of search algorithms and heuristics.
- Benchmarking and reporting for research or development.
- Extensible for new algorithms, heuristics, or reporting formats.

## Extensibility
- Modular design for easy integration of new algorithms or features.
- Well-documented codebase for maintainability and further development.

## Contact
For questions or collaboration opportunities, please reach out via GitHub.
