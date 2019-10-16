import time, sys
import numpy as np
import argparse 

# import matplotlib.pyplot as plt

from blessings import Terminal
term = Terminal()

class GoL:
    def __init__(self, n, m, init_state=None):
        # Initialization of the board
        self.n = n
        self.m = m
        self.board_shape = (n,m)
        # Let's for now assume init_state is given as an array
        self.init_board(init_state)
    
    def init_board(self, init_state):
        if init_state is None:
            self.state = np.random.randint(2, size=self.n*self.m).reshape(self.n,self.m) # random initialization for now
        else:
            self.state = init_state

    def get_state(self):
        return self.state

    def next_cell_state(self,i,j,state):
        # Determine the next state of a single cell
        # TODO: this is extremely crappy way of achieving this goal
        # needs a ton of optimization
        n,m = self.board_shape
        # pull the value of cell, 1 if alive, we'll use this later
        # to sub from the total number of live cells around the target
        val_of_cell = self.state[i,j]
        # This defines the square region we want to pull out
        row_l, row_h = i-1, i+2
        col_l, col_h = j-1, j+2
        # We can't have indices < 0 or >= max value, this 
        # handles sides and corners for us
        if row_l < 0:
            row_l = 0
        if col_l < 0:
            col_l = 0
        if row_h >= n:
            row_h = n-1
        if col_h >= m:
            col_h = m-1
        # This pulls the correct region around target
        region = self.state[row_l:row_h,col_l:col_h]
        # Now we can get the live celll, - our target cell (0 if dead, -1 if alive)
        live_cells = np.count_nonzero(region==1) - val_of_cell
        # 1) Any live cell with fewer than two live neighbours dies, as if by underpopulation.
        # 2) Any live cell with two or three live neighbours lives on to the next generation.
        # 3) Any live cell with more than three live neighbours dies, as if by overpopulation.
        # 4) Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
        # We are implmenting these rules in these ifs
        if val_of_cell == 1:
            if live_cells < 2: 
                return 0
            if live_cells > 3:
                return 0
            else: 
                return 1
        else:
            if live_cells == 3:
                return 1
            else:
                return 0
    
    def run_step(self):
        n,m = self.board_shape
        # we gotta have a full new matrix because 
        # everything happens simultaneously 
        next_state = np.zeros((n,m), dtype=np.int)
        # let's try this neat enumerator
        for ind, val in np.ndenumerate(self.state):
            i,j = ind 
            next_state[i][j] = self.next_cell_state(i,j,self.state)
        # Setting current state as the updated one
        self.state = next_state

def print_board_state(state):
    n,m = state.shape[0], state.shape[1]
    board_string = ""
    for i in range(n):
        row_str = " ".join(map(lambda x: "#" if x == 1 else ".", state[i,:]))
        board_string += row_str + "\n"
    print(term.red+ term.on_white + board_string + term.normal)

def check_end(state):
    # checking if the game ended which happens 
    # when we no longer have live cells
    if np.count_nonzero(state==1) == 0:
        return True
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simple Conway\'s game of life implementation')
    parser.add_argument('-c', '--column', dest='column', type=int, default=30,
                        help='number of columns of the 2D grid')
    parser.add_argument('-r', '--row', dest='row', type=int, default=30,
                        help='number of columns of the 2D grid')
    parser.add_argument('-t', '--time', dest='time', type=int, default=100,
                        help='the number of steps to run the simulation for')
    
    args = parser.parse_args()

    # initialize the game class
    G = GoL(args.row, args.column)
    # setup timer
    timer = 0
    # run until we reach the requested step count
    while timer < args.time:
        print(term.clear())
        print("Current time: {}".format(timer))
        print_board_state(G.get_state())
        G.run_step()
        timer += 1
        if check_end(G.get_state()):
            print("Current time: {}".format(timer))
            print_board_state(G.get_state())
            print("Everybody is dead, hope you are happy")
            break
        time.sleep(0.07)
    print("Congratulations, not everyone is dead, just most of them")
