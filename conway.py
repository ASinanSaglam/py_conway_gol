import time, copy, sys
import numpy as np
import matplotlib.pyplot as plt

from blessings import Terminal
term = Terminal()

def next_cell_state(i,j,state):
    # Determine the next state of a single cell
    # TODO: this is extremely crappy way of achieving this goal
    # needs a ton of optimization
    n,m = state.shape[0], state.shape[1]
    dummy_state = copy.copy(state)
    dummy_state[i,j] = -1
    row_l, row_h = i-1, i+2
    col_l, col_h = j-1, j+2
    if row_l < 0:
        row_l = 0
    if col_l < 0:
        col_l = 0
    if row_h >= n:
        row_h = n-1
    if col_h >= m:
        col_h = m-1
    region = dummy_state[row_l:row_h,col_l:col_h]
    live_cells = np.count_nonzero(region==1)
    dead_cells = np.count_nonzero(region==0)
    # 1) Any live cell with fewer than two live neighbours dies, as if by underpopulation.
    # 2) Any live cell with two or three live neighbours lives on to the next generation.
    # 3) Any live cell with more than three live neighbours dies, as if by overpopulation.
    # 4) Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
    if state[i,j] == 1:
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

def run_step(state):
    n,m = state.shape[0], state.shape[1]
    next_state = np.zeros((n,m), dtype=np.int)
    for i in range(n):
        for j in range(m):
            next_state[i][j] = next_cell_state(i,j,state)
    return next_state

def print_board_state(state):
    n,m = state.shape[0], state.shape[1]
    board_string = ""
    for i in range(n):
        row_str = " ".join(map(lambda x: "#" if x == 1 else ".", state[i,:]))
        board_string += row_str + "\n"
    print(term.red+ term.on_white + board_string + term.normal)

def check_end(state):
    # checking if the game ended
    if np.count_nonzero(state==1) == 0:
        return True
    return False


if __name__ == "__main__":
    # initial size of the system
    n, m = 30, 30 # size of the 2D system
    cur_state = np.random.randint(2, size=n*m).reshape(n,m) # random initialization for now
    t = 100 # number of timesteps to simulate for 
    timer = 0
    
    while timer < t:
        print(term.clear())
        print("Current time: {}".format(timer))
        print_board_state(cur_state)
        cur_state = run_step(cur_state)
        timer += 1
        if check_end(cur_state):
            print("Current time: {}".format(timer))
            print_board_state(cur_state)
            print("Everybody is dead, hope you are happy")
            break
        time.sleep(0.1)
    print("Congratulations, not everyone is dead")
