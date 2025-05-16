from typing import Dict, List, Any
import os

class FileManager:

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
            return None
        
        grid = []
        try:
            with open(filename, 'r') as file:
                for line in file:
                    row = line.strip().split(', ')
                    grid.append([int(cell) if cell.isdigit() else cell for cell in row])
            return grid
        except Exception as e:
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
                    file.write("Limit reached\n\n")
                    return
                
                for row in solution:
                    file.write(', '.join(str(cell) for cell in row))
                    file.write('\n')
                file.write('\n')
        except Exception as e:
            pass

    @staticmethod
    def save_performance(filename: str, performance_data: List[Dict[str, float]], append: bool = False) -> None:
        """
        Save performance data to a file.
        
        Args:
            filename: Path to the output file
            performance_data: List of dictionaries containing performance data
            append: Whether to append to existing file or overwrite
        """
        try:
            # If appending and file exists, read existing data
            existing_data = []
            if append and os.path.exists(filename):
                with open(filename, 'r') as file:
                    lines = file.readlines()
                    if len(lines) > 2:  # Skip header and separator
                        for line in lines[2:]:
                            parts = line.strip().split('|')
                            if len(parts) > 1:
                                test_case = int(parts[0].strip())
                                times = []
                                for t in parts[1:]:
                                    t = t.strip()
                                    if t == "N/A":
                                        times.append(t)
                                    else:
                                        times.append(float(t))
                                data = {
                                    "PySAT": times[0],
                                    "Backtracking": times[1],
                                    "BruteForce": times[2]
                                }
                                existing_data.append(data)

            # Combine existing and new data
            all_data = existing_data + performance_data

            # Write all data
            with open(filename, 'w') as file:
                # Write header
                methods = ["PySAT", "Backtracking", "BruteForce"]
                header = f"{'Test Case':^10} | " + " | ".join(f"{method:^20}" for method in methods)
                file.write(header + "\n")
                file.write("-" * len(header) + "\n")
                
                # Write data
                for idx, data in enumerate(all_data):
                    row = f"{idx:^10} | "
                    for method in methods:
                        time = data[method]
                        if time == "N/A":
                            row += f"{time:^20} | "
                        else:
                            row += f"{time:^20.6f} | "
                    file.write(row + "\n")
        except Exception as e:
            pass