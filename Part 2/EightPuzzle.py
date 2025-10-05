
import random
import sys
import traceback
from collections import deque # for FIFO and LIFO queue
import copy

class PuzzState:

    def __init__(self, state = None ):
        """
        It initializes the PuzzState object when the class is created
        Exception handling is on 

        Returns: 
        PuzzState object

        Arguments:
        state  – state of the puzzle, it should be 3x3 2D matrix 
        """
        try:
            # initialize state as None
            self.state = None
            # if the state is given as argument when creating the object
            # and it is a 2D 3x3 matrix, assign it as the state 
            if state is not None:
                if len(state) == 3 & len(state[0]) == 3:
                    self.state = state
                else:
                    # if it is not a 2D 3x3 natrix, show error
                    print("Error: it is not a 3x3 matrix")
        except Exception as e:
            # in any exception, show the traceback information as an error
            tb = traceback.format_exc()
            print("Error: invalid command:")
            print(tb)

    def cmd(self, command_string):
        """
        It calls the appropriate function according to given command string
        Exception handling is on 

        Arguments:
        command_string  – command given, must be string
        """
        try:
            # take the command name: 
            command = (command_string.split(" "))[0]
            # call the appropriate function according to the command name
            if command == "setState":
                self.set_state(command_string)
            elif command == "setSeed":
                self.set_seed(command_string)
            elif command =="printState":
                self.print_state(self.state)
            elif command == "move":
                [success_move, new_state] = self.move(command_string,self.state,True)
                if success_move:
                    self.state = new_state
            elif command =="scrambleState":
                self.scramble_state(command_string)
            elif (command == "#"):
                self.comment(command_string)
            elif (command == "//"):
                self.comment(command_string)
            elif (command == "solve"):
                # get the name of the algorithm to solve
                algo_name  = (command_string.split(" "))[1]
                max_node = 1000
                # check  whether max node is given
                if (len(command_string.split(" ")) == 3) and (((command_string.split(" "))[2])[0:9] == "maxnodes="):
                    max_node = int(((command_string.split(" "))[2])[9:])
                if algo_name == "DFS":
                    DFS(self, max_node)
                elif algo_name == "BFS":
                    BFS(self, max_node)
                else:
                    print("Error: Invalid Search Algorithm")
            else:
                # if it does not any of theses command: "setsState","printState","move","scrambleState","#","//", show error
                if command != "": # it is done to handle the empty new lines in the test.txt
                    print("Error: invalid command")
        except Exception as e:
            # in any exception, show the traceback information as an error
            tb = traceback.format_exc()
            print("Error: invalid command:")
            print(tb)
    
    def set_state(self, command_str):
        """
        It sets the state of the puzzle by assigning valid state configuration given as argument
        Exception handling is on 

        Arguments:
        command_str  – command given (as a whole not only the arguments), must be string

        Example: "setState 0 1 2 3 4 5 6 7 8"
        "setState" is considered as command name and "0 1 2 3 4 5 6 7 8" considered as state configuration given in this function
        """
        try:
            # from the given command, extract the state configuration
            splitted_command = (command_str.split(" "))[1:10]
            # if the length of the given state config as argument is 9 and state confifuration given is valid (checked by check_state_string funct)
            if (len(splitted_command) == 9) & (self.check_state_string(splitted_command)):
                # convert the string to to 2D 3X3 and assign it as state
                self.state = [list(map(int,splitted_command[i:i+3])) for i in range(0,len(splitted_command), 3)]
            else:
                # if the state configuration given is not valid or have more or less than 9 numbers, show error
                print("Error: invalid puzzle state")
        except Exception as e:
            # in any exception, show the traceback information as an error
            tb = traceback.format_exc()
            print("Error: invalid command:")
            print(tb)

    def print_state(self,state):
        """
        It prints the state of the puzzle as 2D 3x3 matrix
        Exception handling is on 

        Argument:
        state- 2D 3x3 matrix should be given to print the given state
        """
        try:
            # check the state of the puzzle is initialized
            if state is not None:
                puzz_str = ""
                # iterate the state matrix to create a string to print
                for i in range(len(state)):
                    for j in range(len(state[0])):
                        curr_tile = ""
                        # if the tile is blank tile, use space to print it
                        if state[i][j] == 0:
                            curr_tile = " "
                        # otherwise, use the number directly
                        else:
                            curr_tile = state[i][j]
                        # concatanate the tiles in the same row
                        puzz_str = puzz_str + " "+ str(curr_tile)
                    # next row
                    puzz_str = puzz_str + "\n"
                print(puzz_str)
            else:
                # if the function is called before the state is initialized, show error
                print("Error: state is not initialized")
        except Exception as e:
            # in any exception, show the traceback information as an error
            tb = traceback.format_exc()
            print("Error: invalid command:")
            print(tb)

    def move(self, command_str, state_given, print_error):
        """
        It moves the blank tile in one of these directions: up,down,left or right depending on the given command
        Exception handling is on 

        Arguments:
        command_str  – command given (as a whole not only the arguments), must be string
        state_given - state that needs to be moved in the given direction, must be a 2D 3x3 matrix
        print_error - whether the error should be printed or not when the command is invalid, must be bool

        Returns: (bool, next_state)
        bool- if the movement in the given direction is performed return true, otherwise return false
        next_state - the state after the movement is performed is returned if bool is true, otherwise return as None
        """
        try:
            # check the state of the puzzle is initialized
            if state_given is not None:
                # new_state define
                new_state = copy.deepcopy(state_given)
                # finARabesqued the index of the blank tile in the matrix
                [row_blank, col_blank] = self.find_index_tile(state_given,0)
                # according to the index of the blank tile, get the valid directions that the blank tile can be moved
                valid_directions = self.get_possible_movements(row_blank,col_blank)
                # get the direction of the movement from the command string
                splitted_command = (command_str.split(" "))[1:]
                # if the move command is given for one direction and it is in the valid directions, move the blank tile
                if (len(splitted_command) == 1) & (splitted_command[0] in valid_directions):
                    # according to the direction of the movement, swap the values in the matrix
                    if splitted_command[0] == "up":
                        new_state[row_blank][col_blank] = state_given[row_blank-1][col_blank]
                        new_state[row_blank-1][col_blank] = 0
                    elif splitted_command[0] == "down":
                        new_state[row_blank][col_blank] = state_given[row_blank+1][col_blank]
                        new_state[row_blank+1][col_blank] = 0
                    elif splitted_command[0] == "left":
                        new_state[row_blank][col_blank] = state_given[row_blank][col_blank-1]
                        new_state[row_blank][col_blank-1] = 0
                    elif splitted_command[0] == "right":
                        new_state[row_blank][col_blank] = state_given[row_blank][col_blank+1]
                        new_state[row_blank][col_blank+1] = 0
                    return (True,new_state)
                else:
                    # if print_error value is true (in cmd), show error
                    if print_error: 
                        print("Error:Invalid move")
                    # movement is not performed
                    return (False,None)
            else:
                # if print_error value is true (in cmd), show error and the state is not initialized, show error
                if print_error:
                    print("Error: state is not initialized")
                # movement is not performed
                return (False,None)
        except Exception as e:
             # in any exception, show the traceback information as an error
            tb = traceback.format_exc()
            print("Error: invalid command:")
            print(tb)
    
    def set_seed(self,command_str):
        """
        It seeds the random generator

        Arguments:
        command_str  – command given (as a whole not only the arguments), must be string
        """
        # get the seed number
        seed = (command_str.split(" "))[1]
        random.seed(seed)

    def scramble_state(self, command_str):
        """
        It scrambles the puzzle starting from goal state by moving the blank tile randomly n times
        Exception handling is on 

        Arguments:
        command_str  – command given (as a whole not only the arguments), must be string
        """
        try:
            # all directions one can move the blank tile independently from the index of it
            directions = ["up","down","left","right"]
            # get the n- number of times movement is performed
            splitted_command = (command_str.split(" "))[1:]
            if (len(splitted_command) == 1):
                # get the n variable from the command
                n = int(splitted_command[0])
                # initialize goal state
                self.state = [[0,1,2],
                                [3,4,5],
                                [6,7,8]]
                # keep track the count of valid movements made
                count =  0
                while count < n:
                    # randomly choose one of the directions
                    random_direction = random.choice(directions)
                    # create move command string 
                    move_cmd_str = "move " + random_direction
                    # move the current state, give print_error value False 
                    [success,new_state] = self.move(move_cmd_str,self.state,False)
                    # if the movement is performed, increase the number of valid movement (count), print the movement direction and the state (to )
                    if success:
                        count  = count + 1
                        self.state = new_state
                        print(move_cmd_str)
                        self.print_state(self.state)
            else:
                # if the command is given in wrong format print error
                print("Error: Invalid Scramble State")
        except Exception as e:
            # in any exception, show the traceback information as an error
            tb = traceback.format_exc()
            print("Error: invalid command:")
            print(tb)
    
    def comment(self,command_str):
        """
        It ignores the lines or command strings either starts with # or //
        Exception handling is on 

        Arguments:
        command_str  – command given (as a whole not only the arguments), must be string

        Returns:
        uncommended_commands_string which contains lines do not start neither # or //
        """
        try:
            # rearrange the command_str so that remove the lines start with # or //
            # keep track of the lines do not start with # or //
            uncommented_commands = []
            # split the lines in the given command str and iterate over it
            for line in command_str.splitlines():
                # if line is not None and not starts with neither # or //, add it to the uncommented lines
                if line is not None:
                    stripped_line = line.strip()
                    if len(stripped_line) != 0:
                        if not (stripped_line[0] == "#" or (stripped_line[0] == "/" and stripped_line[1] == "/")):
                            uncommented_commands.append(stripped_line)
            # merge uncommented lines in a string and return it
            uncommented_commands_string = "\n".join(uncommented_commands)
            return uncommented_commands_string
        except Exception as e:
            # in any exception, show the traceback information as an error
            tb = traceback.format_exc()
            print("Error: invalid command:")
            print(tb)
        
    def check_state_string(self, str_arr):
        """
        It checks the state configuration given in setState command is valid or not
        Exception handling is on 

        Arguments:
        str_arr – state configuration array given in setState command, must be an array of string
        Example:
        If the command is "setState 1 2 3 4 5 6 7 8 0"
        str_arr = ["1","2","3","4","5","6","7","8","0"] will be given as argument to this function by set_state function

        Returns:
        bool - if the state configuration given is valid return true, otherwise return false
        """
        try:
            # convert string array to int_array
            int_array = [int(num) for num in str_arr ]
            # expected and valid configuration should only contains numbers from 0 to 8
            expected_values = [0,1,2,3,4,5,6,7,8]
            # if the given str_array is the same with the expected_values array when sorted, return true, otherwise return false
            return (sorted(int_array) == expected_values)
        except ValueError:
            return False

    def find_index_tile(self,state,value):
        """
        It finds the index of the given tile number and return it
        Exception handling is on 

        Arguments:
        value – the number value we want to find the index of, must be an int
        state- state that we need to find the index of the given tile, must be an 2D 3x3 matrix

        Returns:
        [row_index, col_index] - iindex of the  value is returned as (row,col) tuple
        """
        try:
            # iterates matrix to find the value in the matrix
            for i, row in enumerate(state):
                if value in row: # if it is in the row, return the index
                    return (i, row.index(value))
            # else if it could not find it return None
            return None
        except Exception as e:
            # in any exception, show the traceback information as an error
            tb = traceback.format_exc()
            print("Error: invalid command:")
            print(tb)

    def get_possible_movements(self, row, col):
        """
        It finds possible movement directions when the row and column number is given
        Exception handling is on 

        Arguments:
        row – the row index of the element, must be an int
        col - the column index of the element, must be an int 

        Returns:
        an array of possible movement directions
        """
        try:
            # initialize all of the movement directions
            possible_movement_directions = ["up","down","left","right"]
            # if row is on the border (0 or 2), remove directions that cannot be possible to move (up and down respectively)
            if row == 0:
                possible_movement_directions.remove("up")
            elif row==2:
                possible_movement_directions.remove("down")
            # if rcolumn is on the border (0 or 2), remove directions that cannot be possible to move (left and right respectively)
            if col == 0:
                possible_movement_directions.remove("left")
            elif col == 2:
                possible_movement_directions.remove("right")
            # return othe rpossible directions
            return possible_movement_directions
        except Exception as e:
            # in any exception, show the traceback information as an error
            tb = traceback.format_exc()
            print("Error: invalid command:")
            print(tb)


class DualOutput:
    def __init__(self, file):
        self.file = file
        self.terminal = sys.stdout

    def write(self, message):
        self.terminal.write(message)  # Write to the terminal
        self.file.write(message)      # Write to the file

    def flush(self):
        # Flush the terminal and file
        self.terminal.flush()
        self.file.flush()

def cmdfile(filename):
    """
    It reads the file with given name and use the cmd function to perform the commands in that file
    It also write output to both terminal and the output.txt file
    Exception handling is on 

    Arguments:
    filename – the name of the files to be read, must be string
    """
     # Open the output file for writing
    with open("output.txt", 'w') as file:
        # Create a DualOutput object
        dual_output = DualOutput(file)
        
        # Redirect stdout to the DualOutput object
        sys.stdout = dual_output
        
        try:
            # Initialize the PuzzState object
            puzzle = PuzzState()
            
            # Read the file with the given filename
            with open(filename, 'r') as infile:
                # Iterate over lines
                for line in infile:
                    # Print every line to both terminal and file
                    print(">>>" + line, end='')  # end='' to avoid adding extra newline
                    
                    # If the line is commented, line_check will be "", otherwise it will be the line itself
                    line_check = puzzle.comment(line)
                    
                    # If line_check is not None, strip it and perform the command by calling cmd function
                    if line_check is not None:
                        puzzle.cmd(line_check.strip())
        
        except Exception as e:
            # Write the exception traceback information to both terminal and file
            tb = traceback.format_exc()
            print("Error: invalid command:")
            print(tb)
        
        # Reset stdout back to the default value
        sys.stdout = sys.__stdout__


def BFS(puzzle_state, max_nodes = 1000):
    """
    It solves the 8-puzzle from the given state using breadth-first search and print the solution in this manner:
    * If the goal state is reached within the node limit, it will print the solution.
    * If the goal state is not reached within the node limit, it will show error.
    
    Exception handling is on 

    Arguments:
    puzzle_state – puzzle state given, must be PuzzState object
    max_nodes - maximum number of the generated puzzle states, must be integer, if it is not given default value is 1000

    Returns:
    bool- True if the solution is found within given max_node limit, False if not found
    """
    # initialize goal state 
    goal_state = PuzzState()
    goal_state.cmd("setState 0 1 2 3 4 5 6 7 8")

    # keep track the number of generated puzzle states
    num_generated_states =  1 # starts with 1 since the root node

    # keep track move sequence
    move_sequence_queue = deque()

    # if the current state is the goal, BFS is done automatically
    if compare_two_states(puzzle_state, goal_state):
        print_search_results(num_generated_states, move_sequence_queue)
        return True


    # make an empty First-In First Out (FIFO) queue for breadth first search
    FIFO_queue = deque()
    
    # define all directions to move the blank tile 
    directions = ["left","right","up","down"]

    # append the root state to the queue and empty array to move sequence queue
    FIFO_queue.append(puzzle_state)
    move_sequence_queue.append([])

    while (FIFO_queue) and (num_generated_states < max_nodes):
        # pop node from the FIFO queue
        curr_node = FIFO_queue.popleft()
        # pop move sequence 
        curr_move_sequence = move_sequence_queue.popleft()

        # update directions according to last movement
        # get the last move
        if len(curr_move_sequence) > 0:
            last_move = curr_move_sequence[len(curr_move_sequence)-1]
            directions = update_directions_bfs(last_move)
   
        # for each child of the curr_node
        for direction in directions:
            # move in the direction
            move_cmd_str = "move " + direction
            # move the current state, give print_error value False 
            [success,new_state] = curr_node.move(move_cmd_str,curr_node.state,False)
            if success: # if the movement in that direction is valid, create child state
                child_state = PuzzState(new_state)

                # increase the num_generated_states
                num_generated_states = num_generated_states + 1

                new_move_sequence = curr_move_sequence + [direction]
                # if child state is the goal state
                if compare_two_states(child_state,goal_state):
                    print_search_results(num_generated_states, new_move_sequence)
                    return True
                else: 
                    # add it to the end of the queue (since we are not doing repeated state checking for this homework no need to check visited states)
                    FIFO_queue.append(child_state)
                    move_sequence_queue.append(new_move_sequence)

    # if the generated states exceeds the max_nodes number given (or 1000 by default), print error
    if num_generated_states >= max_nodes:
        print("Error maxnodes limit ("+str(max_nodes)+") reached")
    
    # return False since could not find a solution
    return False

def DFS(puzzle_state, max_nodes = 1000):
    """
    It solves the 8-puzzle from the given state using depth-first search and print the solution in this manner:
    * If the goal state is reached within the node limit, it will print the solution.
    * If the goal state is not reached within the node limit, it will show error.
    
    Exception handling is on 

    Arguments:
    puzzle_state – puzzle state given, must be PuzzState object
    max_nodes - maximum number of the generated puzzle states, must be integer, if it is not given default value is 1000

    Returns:
    bool- True if the solution is found within given max_node limit, False if not found
    """
    # initialize goal state 
    goal_state = PuzzState()
    goal_state.cmd("setState 0 1 2 3 4 5 6 7 8")

    # keep track the number of generated puzzle states
    num_generated_states =  1 # starts with 1 since the root node

    # keep track move sequence
    move_sequence_queue = deque()

    # if the current state is the goal, DFS is done automatically
    if compare_two_states(puzzle_state, goal_state):
        print_search_results(num_generated_states, move_sequence_queue)
        return True


    # make an empty Last-In First Out (LIFO) queue for depth first search
    LIFO_queue = deque()
    
    # define all directions to move the blank tile 
    directions = ["down","up","right","left"]

    # append the root state to the queue and empty array to move sequence queue
    LIFO_queue.append(puzzle_state)
    move_sequence_queue.append([])

    while (LIFO_queue) and (num_generated_states < max_nodes):
        # pop node from the FIFO queue
        curr_node = LIFO_queue.pop()
        # pop move sequence 
        curr_move_sequence = move_sequence_queue.pop()
        
        if compare_two_states(curr_node, goal_state):
            print_search_results(num_generated_states, curr_move_sequence)
            return True
        
        # update directions according to last movement
        # get the last move
        if len(curr_move_sequence) > 0:
            last_move = curr_move_sequence[len(curr_move_sequence)-1]
            directions = update_directions(last_move)

        # for each child of the curr_node
        for direction in directions:
            # move in the direction
            move_cmd_str = "move " + direction
            # move the current state, give print_error value False 
            [success,new_state] = curr_node.move(move_cmd_str,curr_node.state,False)
            if success: # if the movement in that direction is valid, create child state
                child_state = PuzzState(new_state)

                # increase the num_generated_states
                num_generated_states = num_generated_states + 1

                new_move_sequence = curr_move_sequence + [direction]

                # add it to the end of the queue (since we are not doing repeated state checking for this homework no need to check visited states)
                LIFO_queue.append(child_state)
                move_sequence_queue.append(new_move_sequence)

    # if the generated states exceeds the max_nodes number given (or 1000 by default), print error
    if num_generated_states >= max_nodes:
        print("Error maxnodes limit ("+str(max_nodes)+") reached")
    
    # return False since could not find a solution
    return False

def update_directions(last_move):
    if last_move == "right":
        return ["down","up","right"]
    elif last_move == "left":
        return ["down","up","left"]
    elif last_move == "up":
        return ["up","right","left"]
    elif last_move == "down":
        return ["down","right","left"]
    else:
        return ["down","up","right","left"] 

def update_directions_bfs(last_move):
    if last_move == "right":
        return ["right","up","down"]
    elif last_move == "left":
        return ["left","up","down"]
    elif last_move == "up":
        return ["left","right","up"]
    elif last_move == "down":
        return ["left","right","down"]
    else:
        return ["left","right","up","down"] 

def print_search_results(nodes_created, move_sequence):
    """
    It prints the solution given number of nodes created, solution length and move sequence
    * If the goal state is reached within the node limit, it will print this:
    Example:
    Nodes created during search: 10
    Solution length: 4
    Move sequence:
    move down
    move right
    move up
    move left

    Arguments:
    nodes_created – number of nodes created, must be int
    move_sequence - move sequence, must be int
    """
    # Print information as given template in the homework description
    print("Nodes created during search: " + str(nodes_created))
    print("Solution length: " + str(len(move_sequence)))
    print("Move sequence: ")
    for move in move_sequence:
        print("move " + move)

def compare_two_states(state1, state2):
    """
    It compares the given two states and return True if they are the same, return False if they are different from each other

    Arguments:
    state1- as the first state, must be PuzzState object
    state2- as the second state, must be PuzzState object

    Returns:
    bool- True if they are same, False if they are different 
    """
    return all(row1 == row2 for row1,row2 in zip(state1.state,state2.state))

        
if __name__=="__main__":
    # get the arguments when the program is invoked
    # there should be 2 
    if len(sys.argv) == 2:
        # get the file name that will be used ad test file
        filename = sys.argv[1]
        if ".txt" in filename:
            try: 
                # if it is a txt file, read itwith cmdfile command
                cmdfile(filename)
            except FileNotFoundError:
                print(f"File '{filename}e' not found")
    else:
        # if the program not invoked correctly, show error and how the usage should be 
        print("Error: Usage should be: python3 EightPuzzle.py testcmd.txt")
    


