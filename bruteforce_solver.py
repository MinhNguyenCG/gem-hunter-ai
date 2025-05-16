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
            encoder: The CNF encoder with formula and variable mappings
            max_attempts: Maximum number of attempts before giving up
        """
        super().__init__(grid, encoder)
        self.max_attempts = max_attempts
        self.remaining_attempts = max_attempts
    
    def solve(self) -> Optional[List[int]]:
        """
        Solve the puzzle using a brute force approach.
        
        Returns:
            A model (list of literals) if solution found, None otherwise
        """
        num_vars = self.encoder.next_var_id - 1
        if num_vars == 0:
            return []
            
        # Use binary representations for systematic enumeration
        total_combinations = 1 << num_vars
        
        # Reset attempt counter
        self.remaining_attempts = self.max_attempts
        
        for bits in range(total_combinations):
            # Check if we've exhausted our attempts
            if self.remaining_attempts <= 0:
                return None
                
            self.remaining_attempts -= 1
            
            # Create assignment from bits
            # Each bit position indicates whether a variable is True or False
            assignment = []
            for i in range(num_vars):
                # Extract the i-th bit from the current combination
                assignment.append((bits >> i) & 1 == 1)
            
            # Check if this assignment satisfies all clauses
            if self.is_satisfiable(assignment):
                # Convert to model format (list of literals)
                model = []
                for var_id in range(1, num_vars + 1):
                    # Positive literal for True, negative for False
                    model.append(var_id if assignment[var_id - 1] else -var_id)
                
                return model
        
        # No solution found within the attempt limit
        return None
    
    def is_satisfiable(self, assignment: List[bool]) -> bool:
        """
        Check if an assignment satisfies all clauses in the CNF formula.
        
        Args:
            assignment: List of boolean values for variables (True=trap, False=no trap)
            
        Returns:
            True if the assignment satisfies all clauses
        """
        for clause in self.cnf.clauses:
            # A clause is satisfied if at least one literal is satisfied
            clause_satisfied = False
            
            for literal in clause:
                var_id = abs(literal)
                is_positive = literal > 0
                
                # Skip if the variable is out of range
                if var_id > len(assignment):
                    continue
                
                # Check if this literal satisfies the clause:
                # - Positive literal (var) is satisfied when the variable is True
                # - Negative literal (¬var) is satisfied when the variable is False
                if (is_positive and assignment[var_id - 1]) or (not is_positive and not assignment[var_id - 1]):
                    clause_satisfied = True
                    break
            
            # If no literal satisfies this clause, the assignment is invalid
            if not clause_satisfied:
                return False
                
        # All clauses are satisfied
        return True