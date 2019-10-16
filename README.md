# py_conway_gol
A very simple implementation of [Conways Game of Life](https://www.wikiwand.com/en/Conway%27s_Game_of_Life) that displays the current game state in a terminal

TODO:
1. Allow for custom initialization via a simple input file 
1. Further restructuring of the objects e.g. seperate renderer and game manager 
1. Further optimization for the stepping algorithm
1. Optional: allow custom colors via command line arguments 

Uses [numpy](https://numpy.org) and requires the [blessings](https://github.com/erikrose/blessings) library which is used for terminal output.
