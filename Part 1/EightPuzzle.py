
import random
import sys
import traceback

class PuzzState:
    def __init__(self, state = None ):
        try:
            self.state = None
            if state is not None:
                if len(state) == 3 & len(state[0]) == 3:
                    self.state = state
                else:
                    print("Error: it is not a 3x3 matrix")
        except Exception as e:
            tb = traceback.format_exc()
            print("Error: invalid command:")
            print(tb)



    def cmd(self, command_string):
        try:
            command = (command_string.split(" "))[0]
            if command == "setState":
                self.set_state(command_string)
            elif command =="printState":
                self.print_state()
            elif command == "move":
                self.move(command_string,True)
            elif command =="scrambleState":
                self.scramble_state(command_string)
            elif (command == "#"):
                self.comment(command_string)
            elif (command == "//"):
                self.comment(command_string)
            else:
                if command != "":
                    print("Error: invalid command")
        except Exception as e:
            tb = traceback.format_exc()
            print("Error: invalid command:")
            print(tb)
    
    def set_state(self, command_str):
        try:
            splitted_command = (command_str.split(" "))[1:10]
            if (len(splitted_command) == 9) & (self.check_state_string(splitted_command)):
                # convert it to 2D 3X3
                self.state = [list(map(int,splitted_command[i:i+3])) for i in range(0,len(splitted_command), 3)]
            else:
                print("Error: invalid puzzle state")
        except Exception as e:
            tb = traceback.format_exc()
            print("Error: invalid command:")
            print(tb)

    def print_state(self):
        try:
            if self.state is not None:
                puzz_str = ""
                for i in range(len(self.state)):
                    for j in range(len(self.state[0])):
                        curr_tile = ""
                        if self.state[i][j] == 0:
                            curr_tile = " "
                        else:
                            curr_tile = self.state[i][j]
                        puzz_str = puzz_str + " "+ str(curr_tile)
                    puzz_str = puzz_str + "\n"
                print(puzz_str)
            else:
                print("Error: state is not initialized")
        except Exception as e:
            tb = traceback.format_exc()
            print("Error: invalid command:")
            print(tb)

    def move(self, command_str, print_error):
        try:
            if self.state is not None:
                [row_blank, col_blank] = self.find_index_tile(0)
                valid_directions = self.get_possible_movements(row_blank,col_blank)
                splitted_command = (command_str.split(" "))[1:]
                if (len(splitted_command) == 1) & (splitted_command[0] in valid_directions):
                    if splitted_command[0] == "up":
                        self.state[row_blank][col_blank] = self.state[row_blank-1][col_blank]
                        self.state[row_blank-1][col_blank] = 0
                    elif splitted_command[0] == "down":
                        self.state[row_blank][col_blank] = self.state[row_blank+1][col_blank]
                        self.state[row_blank+1][col_blank] = 0
                    elif splitted_command[0] == "left":
                        self.state[row_blank][col_blank] = self.state[row_blank][col_blank-1]
                        self.state[row_blank][col_blank-1] = 0
                    elif splitted_command[0] == "right":
                        self.state[row_blank][col_blank] = self.state[row_blank][col_blank+1]
                        self.state[row_blank][col_blank+1] = 0
                    return True
                else:
                    if print_error:
                        print("Error:Invalid move")
                    return False
            else:
                if print_error:
                    print("Error: state is not initialized")
                return False
        except Exception as e:
            tb = traceback.format_exc()
            print("Error: invalid command:")
            print(tb)

    def scramble_state(self, command_str):
        try:
            # Seed the random number generator
            random.seed(42)
            directions = ["up","down","left","right"]
            splitted_command = (command_str.split(" "))[1:]
            if (len(splitted_command) == 1):
                # get the n variable from the command
                n = int(splitted_command[0])
                # initialize goal state
                self.state = [[0,1,2],
                                [3,4,5],
                                [6,7,8]]
                count =  0
                while count < n:
                    # randomly choose one of the directions
                    random_direction = random.choice(directions)
                    move_cmd_str = "move " + random_direction
                    # move the current state
                    success = self.move(move_cmd_str,False)
                    if success:
                        count  = count + 1
                        print(move_cmd_str)
                        self.print_state()
            else:
                print("Error: Invalid Scramble State")
        except Exception as e:
            tb = traceback.format_exc()
            print("Error: invalid command:")
            print(tb)
    
    def comment(self,command_str):
        try:
            # rearrange the command_str so that remove the lines start with # or //
            uncommented_commands = []
            for line in command_str.splitlines():
                if line is not None:
                    stripped_line = line.strip()
                    if len(stripped_line) != 0:
                        if not (stripped_line[0] == "#" or (stripped_line[0] == "/" and stripped_line[1] == "/")):
                            uncommented_commands.append(stripped_line)
            uncommented_commands_string = "\n".join(uncommented_commands)
            return uncommented_commands_string
        except Exception as e:
            tb = traceback.format_exc()
            print("Error: invalid command:")
            print(tb)



    def check_state_string(self, str_arr):
        try:
            int_array = [int(num) for num in str_arr ]
            expected_values = [0,1,2,3,4,5,6,7,8]
            return (sorted(int_array) == expected_values)
        except ValueError:
            return False

    def find_index_tile(self,value):
        try:
            for i, row in enumerate(self.state):
                if value in row:
                    return (i, row.index(value))
            return None
        except Exception as e:
            tb = traceback.format_exc()
            print("Error: invalid command:")
            print(tb)

    def get_possible_movements(self, row, col):
        try:
            possible_movement_directions = ["up","down","left","right"]
            if row == 0:
                possible_movement_directions.remove("up")
            elif row==2:
                possible_movement_directions.remove("down")
            
            if col == 0:
                possible_movement_directions.remove("left")
            elif col == 2:
                possible_movement_directions.remove("right")

            return possible_movement_directions
        except Exception as e:
            tb = traceback.format_exc()
            print("Error: invalid command:")
            print(tb)

def cmdfile(filename):
    try:
        # read the filename 
        puzzle = PuzzState()
        with open(filename, 'r') as file:
            for line in file:
                line_check = puzzle.comment(line)
                if line_check is not None:
                    puzzle.cmd(line_check.strip())
    except Exception as e:
            tb = traceback.format_exc()
            print("Error: invalid command:")
            print(tb)
        
if __name__=="__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        if ".txt" in filename:
            try: 
                cmdfile(filename)
            except FileNotFoundError:
                print(f"File '{filename}e' not found")
    else:
        print("Error: Usage should be: python3 EightPuzzle.py testcmd.txt")


