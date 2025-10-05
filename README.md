# Eight Puzzle Solver Suite

This repository provides a comprehensive suite of Eight Puzzle solvers and analysis tools, demonstrating a progression from basic puzzle manipulation to advanced search algorithms and empirical benchmarking. Each part builds on the previous, showcasing problem-solving, algorithm design, and data-driven analysis in a modular and extensible codebase.

## Table of Contents
- [Overview](#overview)
- [Features by Part](#features-by-part)
- [Getting Started](#getting-started)
- [Commands](#commands)
- [Usage](#usage)
- [Applications](#applications)
- [Extensibility](#extensibility)
- [Contact](#contact)

## Overview
The Eight Puzzle is a classic sliding tile puzzle consisting of a 3x3 grid with eight numbered tiles and one empty space. The objective is to rearrange the tiles from an initial configuration to a specified goal configuration by sliding tiles into the empty space, using the minimum number of moves. This repository explores various approaches to solving and analyzing the puzzle, from basic state manipulation to advanced search and benchmarking.

## Features by Part

### Part 1: Basic Solver
- Configurable initial and goal states
- State representation and move generation
- Compatible with various search algorithms
- Traceable output of moves and states

### Part 2: Uninformed Search Algorithms
- Depth-First Search (DFS) and Breadth-First Search (BFS)
- Node limit option for search
- Randomized scrambling with seed control
- Detailed output: nodes created, solution length, move sequence

### Part 3: Heuristics and A* Search
- Multiple heuristic functions (e.g., misplaced tiles, Manhattan distance)
- A* search with selectable heuristics
- Node limit option
- Heuristic evaluation commands

### Part 4: Search Cost Analysis & Branching Factor
- Effective branching factor calculation
- Search cost comparison and benchmarking
- Automated LaTeX table and image generation for reporting
- State generation for systematic benchmarking

## Getting Started
Each part is self-contained in its respective folder (`Part 1`, `Part 2`, `Part 3`, `Part 4`). To run any part, navigate to the desired folder and follow the instructions in its `README.md`.

## Commands
The solver supports a variety of commands, including:

- `setState x1 x2 x3 x4 x5 x6 x7 x8 x9`: Set the puzzle to a specific state (0 = empty space)
- `scrambleState n`: Scramble the puzzle by making `n` random moves
- `setSeed n`: Set the random seed for reproducibility
- `move direction`: Move the empty space (`up`, `down`, `left`, `right`)
- `printState`: Print the current puzzle state
- `solve DFS [maxnodes=N]`: Solve using Depth-First Search
- `solve BFS [maxnodes=N]`: Solve using Breadth-First Search
- `heuristic h1|h2`: Evaluate the current state with a heuristic
- `solve A* h1|h2 [maxnodes=N]`: Solve using A* with a selected heuristic
- `testEBF b h`: Calculate effective branching factor for a uniform tree
- `compareSearchCosts`: Compare search costs across algorithms
- `createsStatesSearchCost d_min d_max step`: Generate states for benchmarking

See the `README.md` in each part for the full list of supported commands and their usage.

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
# ...other commands as needed
```

Replace `/path/to/downloaded/code` with the actual path to the project directory.

## Applications
- Demonstrates and compares uninformed and informed search strategies
- Empirical analysis and benchmarking of search algorithms and heuristics
- Educational tool for problem-solving and AI concepts
- Extensible for new algorithms, heuristics, or reporting formats

## Extensibility
- Modular design for easy integration of new features
- Well-documented codebase for maintainability and further development

## Contact
For questions or collaboration opportunities, please reach out via GitHub.
