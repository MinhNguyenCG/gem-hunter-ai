from file import read_input_file

class Grid:
    __slots__ = ('grid', 'rows', 'cols', '_neighbors_cache')

    def __init__(self, source):
        # Load grid from file path or use provided list
        self.grid = read_input_file(source) if isinstance(source, str) else source
        self.rows = len(self.grid)
        self.cols = len(self.grid[0]) if self.rows else 0
        # Cache neighbors positions for each cell
        self._neighbors_cache = {
            (r, c): self._compute_neighbors(r, c)
            for r in range(self.rows)
            for c in range(self.cols)
        }

    def _compute_neighbors(self, row: int, col: int):
        # Internal: compute valid neighbor positions
        positions = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if (dr or dc):
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        positions.append((nr, nc))
        return positions

    def get_neighbors_positions(self, row: int, col: int):
        # Return cached neighbors or empty list for invalid coords
        return self._neighbors_cache.get((row, col), [])

    def count_surrounding_traps(self, row: int, col: int):
        # Use sum of generator for speed
        return sum(
            1
            for nr, nc in self._neighbors_cache.get((row, col), [])
            if self.grid[nr][nc] == 'T'
        )

    def is_correct_pos(self, row: int, col: int):
        # Validate integer clue matches trap count
        if 0 <= row < self.rows and 0 <= col < self.cols:
            val = self.grid[row][col]
            return isinstance(val, int) and self.count_surrounding_traps(row, col) == val
        return False

    def is_solved(self):
        # All clue cells must be correct
        return all(
            self.is_correct_pos(r, c)
            for r in range(self.rows)
            for c in range(self.cols)
            if isinstance(self.grid[r][c], int)
        )
