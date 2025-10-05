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

# try branching fecator by giving branching factor and tree height to this command
puzzle = PuzzState()
puzzle.cmd("testEBF 2 4")
puzzle.cmd("testEBF 5 5")
puzzle.cmd("testEBF 4 10")

# use already created states to compare them -> tables will be saved to latex folder
puzzle = PuzzState()
puzzle.cmd("compareSearchCosts")

# create states for comparisions - the d values will be [6 8 10 12 14 16 18 20]
puzzle = PuzzState()
puzzle.cmd("createsStatesSearchCost 6 20 2")

# create states for comparisions - the d values will be [5 10 15 20 25]
puzzle.cmd("createsStatesSearchCost 5 25 5")

 
