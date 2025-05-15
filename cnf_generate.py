from typing import Dict, List, Optional, Tuple
from itertools import combinations
from pysat.formula import CNF
from game_grid import GameGrid

class CNFGenerator:
    def __init__(self):
        """Initialize the encoder with empty mappings."""
        self.variable_map: Dict[Tuple[int, int], int] = {}
        self.position_map: Dict[int, Tuple[int, int]] = {}
        self.next_var_id = 1
        self.cnf_formula = CNF()

    def reset(self):
        """Reset the CNFGenerator for a new problem."""
        self.variable_map.clear()
        self.position_map.clear()
        self.next_var_id = 1
        self.cnf_formula = CNF()

    def get_or_create_variable(self, position: Tuple[int, int]) -> int:
        """
        Get an existing variable or create a new one for a position.

        Args:
            position: Grid position (row, col)
            
        Returns:
            Variable ID for the position
        """
        if position not in self.variable_map:
            self.variable_map[position] = self.next_var_id
            self.position_map[self.next_var_id] = position
            self.next_var_id += 1
        return self.variable_map[position]
    
    def get_position(self, var_id: int) -> Optional[Tuple[int, int]]:
        """
        Get the grid position for a variable ID.
        
        Args:
            var_id: Variable ID
            
        Returns:
            Position corresponding to the variable ID or None
        """
        return self.position_map.get(abs(var_id))
    
    def generate_cnf(self, grid: GameGrid) -> CNF:
        """
        Generate CNF constraints from the grid.
        
        Args:
            grid: The game grid
            
        Returns:
            CNF formula representing the puzzle constraints
        """
        self.reset()
        
        # Create variables for empty cells
        for row in range(grid.rows):
            for col in range(grid.cols):
                if grid.data[row][col] == '_':
                    self.get_or_create_variable((row, col))
        
        # For each numbered cell, create constraints for its neighbors
        for row in range(grid.rows):
            for col in range(grid.cols):
                if isinstance(grid.data[row][col], int):
                    self.add_number_constraints(grid, row, col)
        
        # Remove duplicate clauses for efficiency
        self.remove_duplicate_clauses()
    
        return self.cnf_formula
    
    def add_number_constraints(self, grid: GameGrid, row: int, col: int) -> None:
        """
        Add CNF constraints for a numbered cell.
        
        Args:
            grid: The game grid
            row: Row index of the numbered cell
            col: Column index of the numbered cell
        """
        target_traps = grid.data[row][col]
        neighbors = grid.get_neighbors(row, col)
        
        # Filter out neighbors that are numbers (we can only place traps in empty cells)
        valid_neighbors = []

        for n_row, n_col in neighbors:
            cell_value = grid.data[n_row][n_col]
            if not isinstance(cell_value, int):
                valid_neighbors.append((n_row, n_col))
        
        # Map positions to variables
        neighbor_vars = []

        for pos in valid_neighbors:
            row, col = pos
            if grid.data[row][col] == '_':
                var_id = self.get_or_create_variable(pos)
                neighbor_vars.append(var_id)
        
        # Generate "exactly N" constraint
        self.add_exactly_n_constraint(neighbor_vars, target_traps)


    def add_exactly_n_constraint(self, variables: List[int], n: int) -> None:
        """
        Add CNF clauses representing 'exactly n of these variables are true'.
        
        Args:
            variables: List of variable IDs
            n: Number of variables that must be true
        """
        if n > len(variables) or n < 0:
            # Impossible constraint - add empty clause to make CNF unsatisfiable
            self.cnf_formula.append([])
            return
        
        # "At most n" - from any n+1 variables, at least one must be false
        if n < len(variables):
            for combo in combinations(variables, n + 1):
                self.cnf_formula.append([-var for var in combo])

        # "At least n" - from any len(variables)-n+1 variables, at least one must be true
        if n > 0:
            for combo in combinations(variables, len(variables) - n + 1):
                self.cnf_formula.append(list(combo))
        
    def remove_duplicate_clauses(self) -> None:
        """Remove duplicate clauses from the CNF formula for efficiency."""
        unique_clauses = []
        seen_clauses = set()

        for clause in self.cnf_formula.clauses:
            # Sort variables in clauses to normalize, ex: [3, 1, -2] -> [-2, 1, 3]
            sorted_clause = tuple(sorted(clause))

            if sorted_clause not in seen_clauses:
                seen_clauses.add(sorted_clause)      
                unique_clauses.append(clause)      

        # Update the CNF formula with unique clauses
        self.cnf_formula.clauses = unique_clauses


             