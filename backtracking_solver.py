from typing import List, Dict, Optional, Tuple, Set
from game_grid import GameGrid
from cnf_generate import CNFGenerator
from base_solver import BaseSolver

class BacktrackingSolver(BaseSolver):
    
    def __init__(self, grid: GameGrid, encoder: CNFGenerator):
        """
        Initialize the backtracking solver.
        
        Args:
            grid: The game grid to solve
            encoder: The CNF generator with formula
        """
        super().__init__(grid, encoder)
        self.num_vars = self.encoder.next_var_id - 1

    def solve(self) -> Optional[List[int]]:
        """
        Solve using backtracking approach on CNF formula.
        
        Returns:
            A model (list of literals) if solution found, None otherwise
        """
        if self.num_vars == 0:
            return []
        
        # Initialize partial assignment with None values (unassigned)
        assignment = [None] * self.num_vars
        
        # Begin backtracking with variable 1
        if self.backtrack(assignment, 1):
            # Convert to model format (list of literals)
            model = []
            for var_id in range(1, self.num_vars + 1):
                if assignment[var_id - 1]:
                    model.append(var_id)
                else:
                    model.append(-var_id)
            
            return model
        
        return None
    
    def backtrack(self, assignment: List[Optional[bool]], var_idx: int) -> bool:
        """
        Recursive backtracking algorithm implementation.
        
        Args:
            assignment: Current partial assignment of variables
            var_idx: Index of current variable to assign (1-based)
            
        Returns:
            True if a valid solution is found, False otherwise
        """
        # Base case: all variables assigned
        if var_idx > self.num_vars:
            return True
        
        # Try assigning True first then False
        for value in [True, False]:
            assignment[var_idx - 1] = value
            
            # Check if current partial assignment satisfies all relevant clauses
            if self.is_partial_satisfiable(assignment, var_idx):
                # Recursive call with next variable
                if self.backtrack(assignment, var_idx + 1):
                    return True
        
        # Backtrack: reset variable to unassigned
        assignment[var_idx - 1] = None
        return False
    
    def is_partial_satisfiable(self, assignment: List[Optional[bool]], cur_var: int) -> bool:
        """
        Check if a partial assignment satisfies all clauses that could be evaluated.
        Only clauses that have all their variables assigned up to current variable are checked.
        
        Args:
            assignment: Partial assignment of variables (may contain None for unassigned)
            cur_var: Current variable index being assigned (1-based)
            
        Returns:
            True if the partial assignment satisfies all relevant clauses
        """
        # Check each clause
        for clause in self.cnf.clauses:
            # A clause is relevant if all its variables are assigned
            all_assigned = True
            clause_satisfied = False
            
            for literal in clause:
                var_id = abs(literal)
                
                # Skip clauses containing variables we haven't assigned yet
                if var_id > cur_var:
                    all_assigned = False
                    break
                
                is_positive = literal > 0
                var_value = assignment[var_id - 1]
                
                # Check if this literal satisfies the clause
                if (is_positive and var_value) or (not is_positive and not var_value):
                    clause_satisfied = True
                    break
            
            # If all variables in clause are assigned but clause is not satisfied, 
            # the assignment is invalid
            if all_assigned and not clause_satisfied:
                return False
        
        return True