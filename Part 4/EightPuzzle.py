
import random
import sys
import traceback
from collections import deque # for FIFO and LIFO queue
import copy
import heapq
import pickle
import pandas as pd

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
                if algo_name == "DFS":
                    # check  whether max node is given
                    if (len(command_string.split(" ")) == 3) and (((command_string.split(" "))[2])[0:9] == "maxnodes="):
                        max_node = int(((command_string.split(" "))[2])[9:])
                    DFS(self, max_node)
                elif algo_name == "BFS":
                    # check  whether max node is given
                    if (len(command_string.split(" ")) == 3) and (((command_string.split(" "))[2])[0:9] == "maxnodes="):
                        max_node = int(((command_string.split(" "))[2])[9:])
                    BFS(self, max_node)
                elif algo_name == "A*":
                    # get the name of the heuristic
                    heuristic_name = (command_string.split(" "))[2]
                    # check  whether max node is given
                    if (len(command_string.split(" ")) == 4) and (((command_string.split(" "))[3])[0:9] == "maxnodes="):
                        max_node = int(((command_string.split(" "))[3])[9:])
                    # call A_star search function
                    A_star(self, heuristic_name, max_node)
                else:
                    print("Error: Invalid Search Algorithm")
            elif (command == "heuristic"):
                # get the name of the heuristic
                heuristic_name = (command_string.split(" "))[1]
                if(heuristic_name == "h1" or heuristic_name == "h2"):
                    self.heuristic_result(self.state,heuristic_name,True)
                else:
                    print("Error: Invalid Heuristic")
            elif (command == "testEBF"): # as command test EBF by this string "testEBF <branching_factor> <height_tree>" 
                if (len(command_string.split(" ")) == 3 ):
                    # get the branching factor to create tree
                    branching_factor_arg = int((command_string.split(" "))[1])
                    # get the height to create the tree
                    height_arg = int((command_string.split(" "))[2])
                    # calculate total  number of nodes in the tree
                    num_total_nodes = total_nodes_uniform_tree(branching_factor_arg,height_arg)
                    print("Tree has " + str(num_total_nodes) + " nodes" )
                    # test EBF function implemented
                    print("Testing effective branch factor function implemented with N= " + str(num_total_nodes-1) + " and d= " + str(height_arg))
                    estimated_branching_factor = effective_branching_factor(num_total_nodes-1, height_arg)
                    print("Estimated effective branch factor is " + str(estimated_branching_factor))
            elif (command == "createStatesSearchCosts"):
                # get the min and max d and the interval between the trials as the arguments
                if (len(command_string.split(" ")) == 4):
                    # get the branching factor to create tree
                    min_d = int((command_string.split(" "))[1])
                    # get the height to create the tree
                    max_d = int((command_string.split(" "))[2])
                    # get the height to create the tree
                    interval= int((command_string.split(" "))[3])
                    # now, create some puzzle states that have the solution length min_d< d< max_length according to interval
                    # decide the number of rows in the table 
                    d_values = [i for i in range(min_d, max_d + 1, interval)]
                    state_list = []
                    
                    for d in d_values:
                        found = False
                        while not found:
                            self.scramble_state("scrambleState " + str(d))
                            # check with one algorithm whether it has d solution length or not
                            max_node = 2000
                            solved, num_gen_nodes, best_solution = A_star(self, "h2", max_node)
                            solved_dfs, num_gen_nodes_dfs, best_solution_dfs = DFS_comparision(self, 300000, 30)
                            solved_bfs, num_gen_nodes_bfs, best_solution_bfs = BFS(self, 300000)
                            if len(best_solution) == d:  
                                if solved_dfs and solved_bfs:
                                    # add this state to the list of states
                                    state_list.append(self.state)
                                    print("for d=" + str(d) + " state is found"  )
                                    found = True
                                    break
                    # Save to a binary file
                    with open('states.pkl', 'wb') as f:
                        pickle.dump(state_list, f)

            elif (command == "compareSearchCosts"):
                    # Load from pickle
                    with open('states.pkl', 'rb') as f:
                        state_list = pickle.load(f)
                    print(state_list)
                    #create table with those variables
                    columns_len_sol = ["d (BFS)", "d (DFS)", "d (A* h1)","d (A* h2)"]
                    columns_num_nodes =[ "Nodes Generated (BFS)",  "Nodes Generated (DFS)", "Nodes Generated (A* h1)","Nodes Generated (A* h2)"]
                    columns_b_stars = [ "EBF (BFS)", "EBF (DFS)", "EBF(A* h1)", "EBF (A* h2)"]
                    # Create an empty DataFrame with specified columns
                    len_sol_df = pd.DataFrame(columns=columns_len_sol)
                    num_nodes_df = pd.DataFrame(columns=columns_num_nodes)
                    b_stars_df = pd.DataFrame(columns=columns_b_stars)
                    for state_used in state_list:
                        #create PuzzState object with this state
                        curr_state = PuzzState(state_used)
                        # For BFS
                        print("BFS finding solution")
                        solved_bfs, num_nodes_bfs, move_sequence_bfs =BFS(curr_state, 300000)
                        # Length of Solution
                        len_sol_bfs = len(move_sequence_bfs)
                        # Number of Nodes Generated - num_nodes_bfs
                        # Effective Branching Factor
                        b_star_bfs = effective_branching_factor(num_nodes_bfs, len_sol_bfs)
                        

                        # For DFS
                        print("DFS finding solution")
                        solved_dfs, num_nodes_dfs, move_sequence_dfs =DFS_comparision(curr_state, 300000,30)
                        # Length of Solution
                        len_sol_dfs = len(move_sequence_dfs)
                        # Number of Nodes Generated - num_nodes_bfs
                        # Effective Branching Factor
                        b_star_dfs = effective_branching_factor(num_nodes_dfs, 30)
                    
                        # For A* h1
                        print("A* h1 finding solution")
                        solved_A_h1, num_nodes_A_h1, move_sequence_A_h1 =A_star(curr_state, "h1",300000)
                        # Length of Solution
                        len_sol_A_h1 = len(move_sequence_A_h1)
                        # Number of Nodes Generated - num_nodes_bfs
                        # Effective Branching Factor
                        b_star_A_h1 = effective_branching_factor(num_nodes_A_h1, len_sol_A_h1)

                        # For A* h2
                        print("A* h2 finding solution")
                        solved_A_h2, num_nodes_A_h2, move_sequence_A_h2 =A_star(curr_state, "h2",300000)
                        # Length of Solution
                        len_sol_A_h2 = len(move_sequence_A_h2)
                        # Number of Nodes Generated - num_nodes_bfs
                        # Effective Branching Factor
                        b_star_A_h2 = effective_branching_factor(num_nodes_A_h2, len_sol_A_h2)

                        # divide thet tables to ds
                        row_len_sol = [len_sol_bfs, len_sol_dfs, len_sol_A_h1, len_sol_A_h2]
                        # table for num nodes generated
                        row_num_nodes = [num_nodes_bfs, num_nodes_dfs, num_nodes_A_h1,num_nodes_A_h2]
                        # table for b_star
                        row_b_stars = [b_star_bfs, b_star_dfs, b_star_A_h1, b_star_A_h2] 
                        # create row
                        len_sol_df.loc[len(len_sol_df)] = row_len_sol
                        num_nodes_df.loc[len(num_nodes_df)] = row_num_nodes
                        b_stars_df.loc[len(b_stars_df)] = row_b_stars

                    # Save DataFrame as a LaTeX table with custom formatting
                    latex_table_len_sol = len_sol_df.to_latex(index=False,  # To not include the DataFrame index as a column in the table
                        caption="Comparison of ML Model Performance Metrics",  # The caption to appear above the table in the LaTeX document
                        label="tab:model_comparison",  # A label used for referencing the table within the LaTeX document
                        position="htbp",  # The preferred positions where the table should be placed in the document ('here', 'top', 'bottom', 'page')
                        column_format="|l|l|l|l|",  # The format of the columns: left-aligned with vertical lines between them
                        escape=False,  # Disable escaping LaTeX special characters in the DataFrame
                        float_format="{:0.2f}".format)  # Formats floats to two decimal places)
                    latex_table_num_nodes= num_nodes_df.to_latex(index=False,  # To not include the DataFrame index as a column in the table
                        caption="Comparison of ML Model Performance Metrics",  # The caption to appear above the table in the LaTeX document
                        label="tab:model_comparison",  # A label used for referencing the table within the LaTeX document
                        position="htbp",  # The preferred positions where the table should be placed in the document ('here', 'top', 'bottom', 'page')
                        column_format="|l|l|l|l|",  # The format of the columns: left-aligned with vertical lines between them
                        escape=False,  # Disable escaping LaTeX special characters in the DataFrame
                        float_format="{:0.2f}".format)  # Formats floats to two decimal places)
                    latex_table_b_stars= b_stars_df.to_latex(index=False,  # To not include the DataFrame index as a column in the table
                        caption="Comparison of ML Model Performance Metrics",  # The caption to appear above the table in the LaTeX document
                        label="tab:model_comparison",  # A label used for referencing the table within the LaTeX document
                        position="htbp",  # The preferred positions where the table should be placed in the document ('here', 'top', 'bottom', 'page')
                        column_format="|l|l|l|l|",  # The format of the columns: left-aligned with vertical lines between them
                        escape=False,  # Disable escaping LaTeX special characters in the DataFrame
                        float_format="{:0.2f}".format)  # Formats floats to two decimal places)

                    # To save it to a .tex file
                    with open('table_solution_lengths.tex', 'w') as f:
                        f.write(latex_table_len_sol)
                    
                    # To save it to a .tex file
                    with open('table_number_of_nodes_generated.tex', 'w') as f:
                        f.write(latex_table_num_nodes)

                    # To save it to a .tex file
                    with open('table_b_stars.tex', 'w') as f:
                        f.write(latex_table_b_stars)
                    
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
            move_sequence = []
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
                        move_sequence.append(random_direction)
                        self.state = new_state
                        print(move_cmd_str)
                        #self.print_state(self.state)
                        directions = update_directions(random_direction)
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
        
    def heuristic_1(self, state_given, print_result):
        """
        This function will implement the heuristic1 function given in Section 3.6
        h1= the number of misplaced tiles (blank not included). It will be used as the estimated number
        of moves from the current state to the goal state

        Arguments:
        state- state that we need to the number of misplaced tiles, must be an 2D 3x3 matrix
        print_result- whether print the result of the heuristic or not, must be bool

        Returns:
        num_misplaced - number of the misplaced tiles, will be int
        """
        try:
            # initialize the goal state
            goal_state = [[0,1,2],
                        [3,4,5],
                        [6,7,8]]
            # count the number of misplaced tiles
            num_misplaced = 0

            # iterate over 3x3 2D arrays
            for i in range(len(state_given)):
                    for j in range(len(state_given[0])):
                        # if the current tile in the (i,j) location is not the same in the goal state and if the the tile is not blank,
                        # increase the number of misplaced tiles 
                        if (state_given[i][j] != goal_state[i][j]) and (state_given[i][j] != 0):
                            num_misplaced += 1
            if print_result:
                print("Heuristic 1 Result (number of misplaced tiles): " + str(num_misplaced))
            return num_misplaced
        except Exception as e:
            # in any exception, show the traceback information as an error
            tb = traceback.format_exc()
            print("Error: invalid command:")
            print(tb)

    def heuristic_2(self, state_given,print_result):
        """
        This function will implement the heuristic2 function given in Section 3.6
        It will calculate the sum of the distances of the tiles from their goal positions by using city-block distance.

        Arguments:
        state- state that we need to the number of misplaced tiles, must be an 2D 3x3 matrix
        print_result- whether print the result or not, must be bool

        Returns:
        sum_distances -the sum of the distances of the tiles from their goal positions by using city-block distance, will be int 
        """
        try:
            # initialize the goal state
            goal_state = [[0,1,2],
                        [3,4,5],
                        [6,7,8]]

            # initialize the sum of distances
            sum_distances = 0

            # iterate for numbers 1 to 8 
            for num in range(1,9):
                # use find_index_tile function to get the index of the given tile number in given state argument
                [row_given, col_given] = self.find_index_tile(state_given, num )
                # use find_index_tile function to get the index of the given tile number in goal state
                [row_goal, col_goal] = self.find_index_tile(goal_state, num )
                # find the manhattan distance between their indices
                city_block_distance = abs(row_given - row_goal) + abs(col_given-col_goal)
                # add it to the sum_distances
                sum_distances = sum_distances + city_block_distance  
            
            if print_result:
                print("Heuristic 2 Result (sum of the distances from their goal positions): " + str(sum_distances))
            return sum_distances

        except Exception as e:
            # in any exception, show the traceback information as an error
            tb = traceback.format_exc()
            print("Error: invalid command:")
            print(tb)

    def heuristic_result(self,state_given, heuristic_name, print_result):
        """
        This function will get the heuristic value of the given satate with given heuristic name.

        Arguments:
        state_given – puzzle state given, must be 23x3 2D matrix
        heuristic_name - the chosen heuristic name should be "h1" or "h2", must be string
        print_result- whether print the result the heuristic or not, must be bool

        Returns:
        result- it should return the resulte of the heuristic, must be int
        """
        # initialize the result 
        result = -1
        # return value according to the heuristic_name
        if heuristic_name == "h1":
            result= self.heuristic_1(state_given,print_result)
        elif heuristic_name == "h2":
            result = self.heuristic_2(state_given, print_result)
        else:
            print("Invalid Heuristic name")
        return result
    

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


def array_to_tuple(array):
    """
    This function converts a 2D array (list of lists) into a tuple of tuples.
    
    Args:
    array (list of lists): The 2D array to be converted.
    
    Returns:
    tuple: A tuple of tuples representing the converted 2D array.
    """
    return tuple(tuple(row) for row in array)

def A_star(puzzle_state, heuristic_name, max_nodes = 1000):
    """
    It solves the 8-puzzle from the given state using A* search and print the solution in this manner:
    * If the goal state is reached within the node limit, it will print the solution.
    * If the goal state is not reached within the node limit, it will show error.

    Arguments:
    puzzle_state – puzzle state given, must be PuzzState object
    heuristic_name - the chosen heuristic name should be "h1" or "h2"
    max_nodes - maximum number of the generated puzzle states, must be integer, if it is not given default value is 1000

    Returns:
    bool- True if the solution is found within given max_node limit, False if not found
    best_solution- list of move sequences, list of strings
    """
    # initialize goal state 
    goal_state = PuzzState()
    goal_state.cmd("setState 0 1 2 3 4 5 6 7 8")

    # keep track the number of generated puzzle states
    num_generated_states =  1 # starts with 1 since the root node

    # intialize priority queue to store values  (f, g, state, path)
    priority_queue = []

    # initialize the visited hash set
    visited = set()

    # define all directions to move the blank tile 
    # Priority values for directions
    direction_priority = {"left": 0, "right": 1, "up": 2, "down": 3}
    directions = ["left","right","up","down"]

    # push the first state given in to the priority queue
    # in order to do that first find g and h values
    h = puzzle_state.heuristic_result(puzzle_state.state, heuristic_name,False)
    g = 0 # g is 0 initiallly
    # push it to the priority queue
    heapq.heappush(priority_queue, (g + h,-1, g,  [], puzzle_state))

    # we need to keep track of the best solution cost, so the A* should not return
    # when it finds the first selution, best low cost should be return
    # initialize best solution and its cost
    best_solution = None
    best_solution_cost = float('inf')

    # iterate until there is a node inside of the priority queue and be careful about the max_nodes given
    
    while priority_queue and num_generated_states < max_nodes:
        # Get the state with the lowest f = g + h
        f,direction_priority_value, g, path, current_state = heapq.heappop(priority_queue)
        # if the current state is the goal state we need to know
        if compare_two_states(current_state, goal_state):
            # if the solution has lower cost than the best solution cost store it
            if f < best_solution_cost:
                best_solution = path
                best_solution_cost = f
                # print("Potential solution found with cost:", f)
        
        f_values = [item[0] for item in priority_queue] 
        if ((best_solution is not None) and (len(f_values)==0)) or  ((best_solution is not None) and (len(f_values)>0) and (best_solution_cost < min(f_values))):
            print_search_results(num_generated_states, best_solution)
            return True, num_generated_states,best_solution
        # check whether or not the current stat is already visited or not
        if array_to_tuple(current_state.state) in visited:
            # if it is continue for searching
            print("During repeated state check duplicated states are detected")
            continue
        # if it is not in the visited hash set add it
        visited.add(array_to_tuple(current_state.state))

        # update directions according to last movement
        # get the last move
        if len(path) > 0:
            last_move = path[len(path)-1]
            directions = update_directions_bfs(last_move)
        
        # We need the expand the current state node
        for direction in directions:
            # move in the direction
            move_cmd_str = "move " + direction
            # move the current state, give print_error value False 
            [success,new_state] = current_state.move(move_cmd_str,current_state.state,False)
            if success: # if the movement in that direction is valid, check it is visited or not
                if array_to_tuple(new_state) not in visited:
                    # if it is not visited create the child 
                    child_state = PuzzState(new_state)

                    # find the heuristic value of the child state
                    h_child = child_state.heuristic_result(child_state.state, heuristic_name,False)
                    g_child = g + 1
                    # new_path 
                    path_child = path + [direction]
                    # push child to the priority queue
                    heapq.heappush(priority_queue, (g_child + h_child, direction_priority[direction], g_child,  path_child, child_state))

                    # increase the num_generated_states
                    num_generated_states = num_generated_states + 1
                


        # if the generated states exceeds the max_nodes number given (or 1000 by default), print error
        if num_generated_states >= max_nodes:
            print("Error maxnodes limit ("+str(max_nodes)+") reached")
            return False, -1, []

    if (best_solution is not None):
        print_search_results(num_generated_states, best_solution)
        return True, num_generated_states, best_solution
    
    print("No solution found.")
    return False, -1, []
        

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

    # initialize the visited hash set
    visited = set()

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

        # check the repeated states
        if array_to_tuple(curr_node.state) in visited:
            #print("During repeated state check duplicated states are detected")
            continue

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
                    return True, num_generated_states, new_move_sequence
                else: 
                    # add it to the end of the queue (since we are not doing repeated state checking for this homework no need to check visited states)
                    FIFO_queue.append(child_state)
                    move_sequence_queue.append(new_move_sequence)

    # if the generated states exceeds the max_nodes number given (or 1000 by default), print error
    if num_generated_states >= max_nodes:
        print("Error maxnodes limit ("+str(max_nodes)+") reached")
    
    # return False since could not find a solution
    return False, -1, []

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
        return True, num_generated_states, move_sequence_queue


    # make an empty Last-In First Out (LIFO) queue for depth first search
    LIFO_queue = deque()

    # initialize the visited hash set
    visited = set()
    
    # define all directions to move the blank tile 
    directions = ["down","up","right","left"]

    # append the root state to the queue and empty array to move sequence queue
    LIFO_queue.append(puzzle_state)
    move_sequence_queue.append([])

    while (LIFO_queue) and (num_generated_states < max_nodes):
        # pop node from the FIFO queue
        curr_node = LIFO_queue.pop()

        # check the repeated states
        if array_to_tuple(curr_node.state) in visited:
            #print("During repeated state check duplicated states are detected")
            continue

        # pop move sequence 
        curr_move_sequence = move_sequence_queue.pop()
        
        if compare_two_states(curr_node, goal_state):
            print_search_results(num_generated_states, curr_move_sequence)
            return True, num_generated_states , curr_move_sequence

        

         # if it is not in the visited hash set add it
        visited.add(array_to_tuple(curr_node.state))
        
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
            if success and array_to_tuple(new_state) not in visited: # if the movement in that direction is valid, create child state
                #if array_to_tuple(new_state) not in visited:
                # if it is not visited create the child 
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
    return False, -1, []



def DFS_comparision(puzzle_state, max_nodes=1000, max_depth=None):
    """
    It solves the 8-puzzle from the given state using depth-first search and print the solution in this manner:
    * If the goal state is reached within the node limit, it will print the solution.
    * If the goal state is not reached within the node limit, it will show error.
    
    Exception handling is on 

    Arguments:
    puzzle_state – puzzle state given, must be PuzzState object
    max_nodes - maximum number of the generated puzzle states, must be integer, if it is not given default value is 1000
    max_depth - maximum depth limit for the search, must be an integer, if not given defaults to None (no limit)

    Returns:
    bool - True if the solution is found within given max_node limit, False if not found
    num_generated_states - the number of generated states during depth first search
    move_sequence_queue - as the solution of the dfs as the movements done to find the solutionE
    """
    # initialize goal state 
    goal_state = PuzzState()
    goal_state.cmd("setState 0 1 2 3 4 5 6 7 8")

    # keep track the number of generated puzzle states
    num_generated_states = 1  # starts with 1 since the root node

    # keep track move sequence
    move_sequence_queue = deque()

    # if the current state is the goal, DFS is done automatically
    if compare_two_states(puzzle_state, goal_state):
        print_search_results(num_generated_states, move_sequence_queue)
        return True, num_generated_states, move_sequence_queue

    # make an empty Last-In First Out (LIFO) queue for depth first search
    LIFO_queue = deque()

    # initialize the visited hash set
    visited = set()

    # define all directions to move the blank tile 
    directions = ["down", "up", "right", "left"]

    # append the root state to the queue and empty array to move sequence queue
    LIFO_queue.append((puzzle_state, 0))  # Include depth in the state
    move_sequence_queue.append([])

    while LIFO_queue and num_generated_states < max_nodes:
        # pop node from the FIFO queue
        curr_node, curr_depth = LIFO_queue.pop()

        # check if the current depth exceeds max_depth
        if max_depth is not None and curr_depth >= max_depth:
            continue  # skip this node if depth exceeds limit

        # check the repeated states
        if array_to_tuple(curr_node.state) in visited:
            continue

        # pop move sequence 
        curr_move_sequence = move_sequence_queue.pop()

        if compare_two_states(curr_node, goal_state):
            print_search_results(num_generated_states, curr_move_sequence)
            return True, num_generated_states, curr_move_sequence

        # if it is not in the visited hash set add it
        visited.add(array_to_tuple(curr_node.state))

        # update directions according to last movement
        # get the last move
        if len(curr_move_sequence) > 0:
            last_move = curr_move_sequence[-1]
            directions = update_directions(last_move)

        # for each child of the curr_node
        for direction in directions:
            # move in the direction
            move_cmd_str = "move " + direction
            # move the current state, give print_error value False 
            [success, new_state] = curr_node.move(move_cmd_str, curr_node.state, False)
            if success and array_to_tuple(new_state) not in visited:  # if valid and not visited
                child_state = PuzzState(new_state)

                # increase the num_generated_states
                num_generated_states += 1

                new_move_sequence = curr_move_sequence + [direction]

                # add it to the end of the queue along with the new depth
                LIFO_queue.append((child_state, curr_depth + 1))  # Increment depth
                move_sequence_queue.append(new_move_sequence)

    # if the generated states exceeds the max_nodes number given (or 1000 by default), print error
    if num_generated_states >= max_nodes:
        print("Error: maxnodes limit (" + str(max_nodes) + ") reached")
    
    # return False since could not find a solution
    return False, -1, []

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

def effective_branching_factor(N, d):
    """
    Calculate the effective branching factor b* that satisfies, iterativeky by using binary serach logic:
    
    N + 1 = 1 + b* + (b*)^2 + ... + (b*)^d
    
    Arguments:
    N -- Total number of nodes generated
    d -- Depth of the solution

    Returns:
    b_star -- The estimated effective branching factor
    """
    try:
        # Since we are going to estimate the branching factor, we need to give a tolerance value to that estimate 
        # and a iteration number if it will not converge
        # Initialize tolerance and maximum iteration number
        tolerance=1e-16
        max_iter=200000

        # Initialize the range of the binary value can take as value [1,N] since it has N branch at most
        lowest_b_star_value = 1
        highest_b_star_value = N

        # Iterate max iteration time to find the effective branching factor
        for i in range(max_iter):
            # take the average of the lowest and highest b* values possible
            b_star = (lowest_b_star_value + highest_b_star_value) / 2 

            # calculate the (N+1) value at the right hand side of the equation   N + 1 = 1 + b* + (b*)^2 + ... + (b*)^d with the b* we have
            N_plus_one_estimated = 1
            for depth in range(1,d+1): 
                N_plus_one_estimated = N_plus_one_estimated + (b_star ** depth )
            
            # If the effective branching factor we used calculates N+1 estimated close enough to the actual N+1 value, return it
            if abs(N_plus_one_estimated - (N + 1)) < tolerance:  
                return b_star
            
            if N_plus_one_estimated < N + 1:  # If our estimate for N+1 is smaller than the actual N+1, we need to increase the branching factor value
                # If we set the lowest possible branching factor value to current branching factor value, thanks to binary search nature of this algorithm we
                # increase the next b_star value we tried automatically
                lowest_b_star_value = b_star 

            else:  # If our estimate for N+1 is larger than the actual N+1, we need to decrease the branching factor value
                # If we set the highest possible branching factor value to current branching factor value, thanks to binary search nature of this algorithm we
                # decrease the next b_star value we tried automatically
                highest_b_star_value = b_star

                
        return b_star  # If we finished maximum iteration return the value found so far, it may not converge 
    except Exception as e:
            # Write the exception traceback information to both terminal and file
            tb = traceback.format_exc()
            print("Error in effective branch computing:")
            print(tb)

# This class is implemented in order to test the effective branching factor function
# It is a basic tree node, we will use it to create uniform trees
class TreeNode:
    # define value and children of the node as an array
    def __init__(self, value):
        self.value = value
        self.children = []
    
    # in order to add children to the node, we need a function
    def add_child(self, child_node):
        self.children.append(child_node)


def total_nodes_uniform_tree(branching_factor, height):
    """
    This function will calculate the total numbers in a unifrom tree given branching_factor and height. It is calculated as:
        # nodes = (b**(h + 1) - 1) / (b - 1) where b is branching factor and  h is height

    Arguments:
    branching_factor -- the number of branches every node has in the UNIFORM TREE, must be int
    height --  the height of the tree, must be int

    Returns:
    total_node_numbers -- the total node numers in a uniform tree
    """
    if branching_factor == 1:
        return height + 1  # Special case: a degenerate tree (like a linked list)
    
    total_node_numbers = (branching_factor**(height + 1) - 1) // (branching_factor - 1)
    
    return total_node_numbers
        
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
    
 


