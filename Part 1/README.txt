* testcmds.txt is the test file used i order to test the program. It also contains some error states to check the desired edge cases etc.

* output.txt file is the output file of the terminal when I run the testcmds.txt file.

* In order to execute with a test file named testcmds.txt run this:

python3 EightPuzzle.py testcmds.txt


* In order to execute individual commands from an interactive prompt:

python3
import sys
sys.path.append("/path/to/downloaded/code")
from EightPuzzle import PuzzState
puzzle = PuzzState()
puzzle.cmd("setState 7 2 4 5 0 6 8 3 1")
puzzle.cmd("printState")
