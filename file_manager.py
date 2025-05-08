from typing import Dict, List, Any
import os
from venv import logger

class FileManager:
    """Handles all file I/O operations for the gem hunter game."""
    
    @staticmethod
    def load_grid(filename: str) -> List[List[Any]]:
        """
        Load a grid from a file.
        
        Args:
            filename: Path to the input file
            
        Returns:
            The loaded grid or None if file doesn't exist
        """
        if not os.path.exists(filename):
            logger.error(f"File {filename} does not exist")
            return None
        
        grid = []
        try:
            with open(filename, 'r') as file:
                for line in file:
                    row = line.strip().split(', ')
                    grid.append([int(cell) if cell.isdigit() else cell for cell in row])
            return grid
        except Exception as e:
            logger.error(f"Error reading file {filename}: {e}")
            return None
    
    @staticmethod
    def save_solution(solution: List[List], filename: str, method_name: str, overwrite: bool = False) -> None:
        """
        Save a solution to a file.
        
        Args:
            solution: The solution grid to save
            filename: Path to the output file
            method_name: Name of the solving method
            overwrite: Whether to overwrite the file if it exists
        """
        try:
            with open(filename, 'w' if overwrite else 'a') as file:
                file.write(f"{method_name}:\n")
                if not solution:
                    file.write("No solution\n\n")
                    return
                
                for row in solution:
                    file.write(', '.join(str(cell) for cell in row))
                    file.write('\n')
                file.write('\n')
            logger.info(f"Solution saved to {filename}")
        except Exception as e:
            logger.error(f"Error writing solution to {filename}: {e}")