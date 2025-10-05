* testcmds.txt is the test file used i order to test the program. It also contains some error states to check the desired edge cases etc.

* output_ixk238.txt file is the output file of the terminal when I run the testcmds.txt file.

* every time you run it with test_cmds.txt, it is both showing output in terminal and write it to output.txt file.

* In order to execute with a test file named testcmds.txt run this:

python3 EightPuzzle.py testcmds.txt


* In order to execute individual commands from an interactive prompt:
python3
>>> import sys
>>> sys.path.append("/path/to/downloaded/code")
>>> from EightPuzzle import PuzzState
>>> puzzle = PuzzState()
>>> puzzle.cmd("setState 0 1 2 3 4 5 6 7 8")
>>> puzzle.cmd("printState")
   1 2
 3 4 5
 6 7 8

>>> puzzle.cmd("move right")
>>> puzzle.cmd("printState")
 1   2
 3 4 5
 6 7 8

>>> puzzle.cmd("move right")
>>> puzzle.cmd("printState")
 1 2  
 3 4 5
 6 7 8

>>> puzzle.cmd("solve DFS")
Nodes created during search: 5
Solution length: 2
Move sequence: 
move left
move left
>>> puzzle.cmd("solve BFS")
Nodes created during search: 4
Solution length: 2
Move sequence: 
move left
move left
>>> puzzle.cmd("solve DFS maxnodes=3")
Error maxnodes limit (3) reached
>>> puzzle.cmd("solve BFS maxnodes=3")
Error maxnodes limit (3) reached
>>> 
