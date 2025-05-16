from pysat.solvers import Solver as PySatSolverRaw
from typing import List, Optional
from base_solver import BaseSolver

class PySATSolver(BaseSolver):
    def solve(self) -> Optional[List[int]]:
        # Initialize the solver
        solver = PySatSolverRaw()
        # Append the CNF formula to the solver
        solver.append_formula(self.cnf)
        # Solve the CNF formula
        if solver.solve():
            # Return the model if the CNF formula is satisfiable
            return solver.get_model()
        return None