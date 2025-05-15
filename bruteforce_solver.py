from typing import List, Optional
from game_grid import GameGrid
from cnf_generate import CNFGenerator
from base_solver import BaseSolver

class BruteForceSolver(BaseSolver):
    """Solver using brute force approach."""
    
    def __init__(self, grid: GameGrid, encoder: CNFGenerator, max_attempts: int = 1000000):
        """
        Initialize the brute force solver.
        
        Args:
            grid: The game grid to solve
            encoder: The logic encoder with CNF formula
            max_attempts: Maximum number of attempts before giving up
        """
        super().__init__(grid, encoder)
        self.max_attempts = max_attempts
        self.remaining_attempts = max_attempts
        self.method_name = "Brute Force"
    
    def solve(self) -> Optional[List[int]]:
        """
        Solve using brute force approach.
        
        Returns:
            A model (list of literals) if solution found, None otherwise
        """
        num_vars = self.encoder.next_var_id - 1
        if num_vars == 0:
            return []
            
        # Reset attempt counter
        self.remaining_attempts = self.max_attempts
        
        # Use binary representations for systematic enumeration
        total_combinations = 1 << num_vars
        max_to_try = min(total_combinations, self.max_attempts)
        
        for bits in range(max_to_try):
            self.remaining_attempts -= 1
            
            # Create assignment from bits
            assignment = [bool((bits >> i) & 1) for i in range(num_vars)]
            
            # Check if this assignment satisfies all clauses
            if self.is_satisfiable(assignment):
                # Convert to model format (list of literals)
                model = []
                for var_id in range(1, num_vars + 1):
                    model.append(var_id if assignment[var_id - 1] else -var_id)
                
                return model
        
        return None
    
    def is_satisfiable(self, assignment: List[bool]) -> bool:
        """
        Check if an assignment satisfies all clauses.
        
        Args:
            assignment: List of boolean values for variables
            
        Returns:
            True if the assignment satisfies all clauses
        """
        for clause in self.cnf.clauses:
            # A clause is satisfied if at least one literal is satisfied
            satisfied = False
            
            for literal in clause:
                var_id = abs(literal)
                is_positive = literal > 0
                
                # Skip if the variable is out of range
                if var_id > len(assignment):
                    continue
                
                # Check if this literal satisfies the clause
                if (is_positive and assignment[var_id - 1]) or (not is_positive and not assignment[var_id - 1]):
                    satisfied = True
                    break
            
            # If no literal satisfies this clause, the assignment is invalid
            if not satisfied:
                return False
                
        return True