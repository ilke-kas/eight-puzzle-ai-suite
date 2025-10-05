* testcmds.txt is the test file used i order to test the program. It also contains some error states to check the desired edge cases etc.

* output_ixk238.txt file is the output file of the terminal when I run the testcmds.txt file.

* every time you run it with test_cmds.txt, it is both showing output in terminal and write it to output.txt file.

* In order to execute with a test file named testcmds.txt run this:

python3 EightPuzzle.py testcmds.txt


* In order to execute individual commands from an interactive prompt:
python3
import sys
sys.path.append("/path/to/downloaded/code")
from EightPuzzle import PuzzState

# try heuristics (Exercise 4)
puzzle = PuzzState()
puzzle.cmd("setState 0 1 2 3 4 5 6 7 8")
puzzle.cmd("printState")


puzzle.cmd("heuristic h1")
puzzle.cmd("heuristic h2")

puzzle.cmd("scrambleState 5")

puzzle.cmd("heuristic h1")
puzzle.cmd("heuristic h2")

# try A_star (Exercise 5-6)
puzzle = PuzzState()
puzzle.cmd("setState 0 1 2 3 4 5 6 7 8")
puzzle.cmd("solve A* h1 maxnodes=10000")

puzzle.cmd("scrambleState 5")
puzzle.cmd("solve A* h2")


 
