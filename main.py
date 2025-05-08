import os, logging
from file_manager import FileManager
from game_grid import GameGrid
from cnf_generate import CNFGenerator
from pysat_solver import PySATSolver
from bruteforce_solver import BruteForceSolver
from venv import logger

def process_testcase(i: int):
    input_file = f"testcases/input_{i}.txt"
    output_file = f"testcases/output_{i}.txt"

    grid = GameGrid.from_file(input_file)
    encoder = CNFGenerator()
    encoder.generate_constraints(grid)

    bf = BruteForceSolver(grid, encoder)
    #dpll = DPLLSolver(grid, encoder)
    pysat = PySATSolver(grid, encoder)

    # for solver, name, ow in [(bf, "BruteForce", True),
    #                          (dpll, "DPLL", False),
    #                          (pysat, "PySAT", False)]:
    #     solver.save_solution(output_file, name, ow)

    bf.save_solution(output_file, "BruteForce", False)
    pysat.save_solution(output_file, "PySAT", False)
    return {
        # "BruteForce": bf.execution_time,
        # "DPLL": dpll.execution_time,
        "PySAT": pysat.execution_time
    }

def main():
    result = process_testcase(2)
    logger.info("Done all cases.")

if __name__ == "__main__":
    main()