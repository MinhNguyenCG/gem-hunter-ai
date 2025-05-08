import time, logging
from copy import deepcopy
from typing import Any, List, Optional
from game_grid import GameGrid
from cnf_generate import CNFGenerator
from file_manager import FileManager
from venv import logger
"""Base class for all solvers."""


class BaseSolver:
    def __init__(self, grid: GameGrid, encoder: CNFGenerator):
        self.grid = deepcopy(grid)
        self.encoder = encoder
        self.cnf = encoder.cnf_formula
        self.solution = None
        self.execution_time = 0.0

    def solve(self) -> Optional[List[int]]:
        """Solve the puzzle and return a model if found."""
        raise NotImplementedError("Each solver must implement the solve method")

    def apply_solution(self, model: List[int]) -> List[List[Any]]:
        """Apply a solution model to create a solved grid."""
        if not model:
            return None
            
        solution_grid = deepcopy(self.grid.data)
        
        # Apply the model
        for var in model:
            pos = self.encoder.get_position(var)
            if pos:
                # Positive variables are traps, negative are gems
                solution_grid[pos[0]][pos[1]] = 'T' if var > 0 else 'G'
        
        # Fill in any remaining empty cells as gems by default
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                if solution_grid[row][col] == '_':
                    solution_grid[row][col] = 'G'
        
        return solution_grid

    def get_solution(self) -> List[List[Any]]:
        """Get the solution, solving if necessary."""
        if self.solution is None:
            start_time = time.time()
            model = self.solve()
            self.execution_time = time.time() - start_time
            
            self.solution = self.apply_solution(model)
        
        return self.solution

    def save_solution(self, filename: str, method_name: str, overwrite: bool = False) -> None:
        """Save the solution to a file."""
        solution = self.get_solution()
        
        # Verify solution first
        if solution:
            verification_grid = GameGrid(solution)
            status = "satisfiable" if verification_grid.is_solved() else "not satisfiable"
            logger.info(f"{method_name}: {status}")
            
            # Only save if solution is valid
            if status == "satisfiable":
                FileManager.save_solution(solution, filename, method_name, overwrite)
        else:
            logger.info(f"{method_name}: No solution found")