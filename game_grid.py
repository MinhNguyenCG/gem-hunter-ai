from dataclasses import dataclass, field
from typing import List, Any, Tuple
from file_manager import FileManager

@dataclass
class GameGrid:
    """Represents a gem hunter game grid with enhanced functionality."""
    data: List[List[Any]]
    rows: int = field(init=False)
    cols: int = field(init=False)

    def __post_init__(self):
            self.rows = len(self.data)
            self.cols = len(self.data[0]) if self.rows > 0 else 0
     
    @classmethod
    def from_file(cls, filename: str) -> 'GameGrid':
        """Create a GameGrid from a file."""
        grid_data = FileManager.load_grid(filename)
        if grid_data is None:
            # Create an empty grid as fallback
            return cls([[]])
        return cls(grid_data)
    

    def get_value(self, row: int, col: int) -> Any:
        """Get the value at a specific position."""
        if self.is_valid_position(row, col):
            return self.data[row][col]
        return None
    
    def set_value(self, row: int, col: int, value: Any) -> bool:
        """Set the value at a specific position."""
        if self.is_valid_position(row, col):
            self.data[row][col] = value
            return True
        return False
    

    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if a position is valid on the grid."""
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Get all neighboring positions."""
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                    
                new_row, new_col = row + i, col + j
                if self.is_valid_position(new_row, new_col):
                    neighbors.append((new_row, new_col))
        return neighbors
    
    