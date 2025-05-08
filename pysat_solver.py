from pysat.solvers import Solver as PySatSolverRaw
from typing import List, Optional
from base_solver import BaseSolver

class PySATSolver(BaseSolver):
    def solve(self) -> Optional[List[int]]:
        solver = PySatSolverRaw()
        solver.append_formula(self.cnf)
        if solver.solve():
            return solver.get_model()
        return None