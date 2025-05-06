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
    