import os
from file_manager import FileManager
from game_grid import GameGrid
from cnf_generate import CNFGenerator
from pysat_solver import PySATSolver
from bruteforce_solver import BruteForceSolver
from gui import GameGUI


def main():
    # Initialize and run the GUI
    gui = GameGUI()
    gui.run()

if __name__ == "__main__":
    main()