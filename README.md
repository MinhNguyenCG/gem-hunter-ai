# Gem Hunter AI 🎮

## 👥 Author
- 22120238 - Nguyễn Minh Nguyên

## 📜 Description
This project is a Gem Hunter game implemented in Python using **Pygame** and **python-sat**, featuring multiple solving algorithms:
- PySAT Solver: Using SAT solving techniques
- Backtracking Solver: Using backtracking algorithm
- Brute Force Solver: Using exhaustive search

## 🚀 How to Run
### 0. Prerequisite: Install Python

Before installing dependencies or running the game, make sure you have Python 3.11 (or later) installed on your system:

- **Windows**  
  1. Go to the official Python downloads page: https://www.python.org/downloads/windows/
  2. Download the latest "Windows installer (64-bit)".
  3. Run the installer.

- **macOS**  
  1. Visit https://www.python.org/downloads/macos/ and download the latest macOS installer.
  2. Open the `.pkg` file and follow the prompts to complete installation.  
  3. Alternatively, you can install via Homebrew:  
     ```bash
     brew install python
     ```

### 1. Install dependencies
You can install all required packages using pip:

```bash
pip install -r requirements.txt
``` 

### 2. Run the game
After installing the dependencies, run:
```bash
py main.py
``` 

## 📁 Project Structure
```
gem-hunter-ai/
├── testcase/                  # Input, output and performance
├── game_grid.py               # Manage matrix
├── cnf_generate.py            # CNF formula generation
├── file_manager.py            # File handling utilities
├── base_solver.py             # Interface for algorithms
├── pysat_solver.py            # Pysat solver
├── backtracking_solver.py     # Backtracking solver
├── bruteforce_solver.py       # Bruteforce solver
├── gui                        # User interface
├── main.py                    # Game entry point
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```