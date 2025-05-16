import pygame
import sys
import os
from game_grid import GameGrid
from bruteforce_solver import BruteForceSolver
from cnf_generate import CNFGenerator
from pysat_solver import PySATSolver
from backtracking_solver import BacktrackingSolver
from file_manager import FileManager

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (238, 238, 238)
LIGHT_GRAY = (220, 220, 220)
BLUE = (78, 215, 241)
RED = (255, 0, 0)
GREEN = (57, 224, 31)
YELLOW = (255, 255, 0)
PURPLE = (180, 60, 220)
DARK_GREEN = (73, 161, 26)

# Font
FONT = pygame.font.SysFont('Calibri', 16)
FONT.set_bold(True)
TITLE_FONT = pygame.font.SysFont('Calibri', 20)
TITLE_FONT.set_bold(True)
SMALL_FONT = pygame.font.SysFont('Calibri', 14)

class Button:
    def __init__(self, x, y, width, height, text, color=GRAY):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.is_hovered = False
        self.active = False

    def draw(self, screen):
        # Determine color based on hover and active state
        if self.active:
            # Darken the color by 40% for active state
            color = (
                int(self.color[0] * 0.7),
                int(self.color[1] * 0.7),
                int(self.color[2] * 0.7)
            )
        elif self.is_hovered:
            # Lighten the color by 20% for hover state
            color = (
                min(int(self.color[0] * 1.2), 255),
                min(int(self.color[1] * 1.2), 255),
                min(int(self.color[2] * 1.2), 255)
            )
        else:
            color = self.color
            
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        text_surface = FONT.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class GameGUI:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Gem Hunter Solver")
        
        # Create size selection buttons
        button_width = 120
        button_height = 40
        spacing = 20
        
        matrix_sizes = ["Input 1: 3x3", "Input 2: 5x5", "Input 3: 7x7", "Input 4: 9x9", "Input 5: 11x11", "Input 6: 20x20"]
        self.testcase_buttons = [
            Button(20 + i * (button_width + spacing), 20,
                  button_width, button_height, 
                  matrix_sizes[i])
            for i in range(len(matrix_sizes))
        ]
        
        # Process and Open Output buttons
        self.process_button = Button(20, 80, button_width, button_height, "Process", GREEN)
        self.open_output_button = Button(160, 80, button_width, button_height, "Open Output", BLUE)
        self.clear_output_button = Button(300, 80, button_width, button_height, "Clear Output", RED)
        self.process_all_button = Button(440, 80, button_width, button_height, "Process All", YELLOW)
        self.clear_all_output_button = Button(580, 80, button_width, button_height, "Clear All Output", YELLOW)

        # Algorithm selection buttons
        self.pysat_button = Button(720, 630, button_width, button_height, "PySAT", YELLOW)
        self.backtracking_button = Button(920, 630, button_width, button_height, "Backtracking", YELLOW)
        self.bruteforce_button = Button(1120, 630, button_width, button_height, "Bruteforce", YELLOW)
        
        self.algorithm_buttons = [self.pysat_button, self.backtracking_button, self.bruteforce_button]
        
        # State variables
        self.current_testcase = None
        self.grid = None
        self.selected_algorithm = "PySAT"  # Default algorithm
        self.pysat_button.active = True
        self.status_message = ""
        self.status_message_color = DARK_GREEN
        self.solution_grid = None
        self.solution_text = ""

    def load_testcase(self, testcase_num):
        input_file = f"testcases/input_{testcase_num}.txt"
        if os.path.exists(input_file):
            self.grid = GameGrid.from_file(input_file)
            self.current_testcase = testcase_num
            self.status_message = ""
            self.load_solution()

    def process_testcase(self):
        if self.grid and self.current_testcase:
            output_file = f"testcases/output_{self.current_testcase}.txt"
            performance_file = "testcases/performance.txt"
            
            if os.path.exists(output_file):
                # Update status message
                self.status_message = "Output file already exists!"
                self.status_message_color = RED
                return
            
            try:
                encoder = CNFGenerator()
                encoder.generate_cnf(self.grid)
                
                # Dictionary to store performance data
                performance_data = {
                    "test_case": self.current_testcase,
                    "PySAT": None,
                    "Backtracking": None,
                    "BruteForce": None
                }
                
                # Run solvers and get their execution times
                pysat = PySATSolver(self.grid, encoder)
                pysat.get_solution() 
                if pysat.solution is None:
                    performance_data["PySAT"] = "N/A"
                else:
                    performance_data["PySAT"] = pysat.execution_time * 1000  # Convert to ms
                pysat.save_solution(output_file, "PySAT", False)
                
                bt = BacktrackingSolver(self.grid, encoder)
                bt.get_solution() 
                if bt.solution is None:
                    performance_data["Backtracking"] = "N/A"
                else:
                    performance_data["Backtracking"] = bt.execution_time * 1000  # Convert to ms
                bt.save_solution(output_file, "Backtracking", False)
                
                bf = BruteForceSolver(self.grid, encoder)
                bf.get_solution() 
                if bf.solution is None:
                    performance_data["BruteForce"] = "N/A"
                else:
                    performance_data["BruteForce"] = bf.execution_time * 1000  # Convert to ms
                bf.save_solution(output_file, "BruteForce", False)
                
                # Save performance data (append mode)
                FileManager.save_performance(performance_file, [performance_data], True)
                
                # Update status message with execution times
                time_msg = f"Testcase {self.current_testcase} - PySAT: {pysat.execution_time*1000:.2f}ms, "
                if bt.solution is None:
                    time_msg += f"Backtracking: N/A, "
                else:
                    time_msg += f"Backtracking: {bt.execution_time*1000:.2f}ms, "
                if bf.solution is None:
                    time_msg += f"BruteForce: N/A"
                else:
                    time_msg += f"BruteForce: {bf.execution_time*1000:.2f}ms"
                self.status_message = time_msg
                self.status_message_color = DARK_GREEN
                
                self.load_solution()  # Load the new solution
            except Exception as e:
                self.status_message = f"Error processing testcase: {str(e)}"
                self.status_message_color = RED

    def load_solution(self):
        if not self.current_testcase:
            return

        output_file = f"testcases/output_{self.current_testcase}.txt"
        if not os.path.exists(output_file):
            self.solution_grid = None
            self.solution_text = ""
            return

        # Read output file
        with open(output_file, 'r') as f:
            content = f.read()

        # Split content by algorithm
        sections = content.split('\n\n')
        
        # Parse based on selected algorithm
        self.solution_grid = []
        
        for section in sections:
            if section.startswith(self.selected_algorithm):
                lines = section.strip().split('\n')
                for line in lines[1:]:  # Skip the algorithm name line
                    if line:
                        if line[0] not in ['T', 'G', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                            self.solution_text = line
                        else:
                            self.solution_grid.append(line.split(', '))
                break

    def open_output_file(self):
        if self.current_testcase:
            # Get absolute path of the output file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            output_file = os.path.join(current_dir, f"testcases/output_{self.current_testcase}.txt")
            
            try:
                if os.path.exists(output_file):
                    # Try to open with default system application
                    if sys.platform == 'win32':
                        os.startfile(output_file)
                    else:
                        import subprocess
                        subprocess.run(['xdg-open', output_file])
                else:
                    self.status_message = f"Output file not found at: {output_file}"
                    self.status_message_color = RED
            except Exception as e:
                self.status_message = f"Error opening file: {str(e)}"
                self.status_message_color = RED

    def clear_output_file(self):
        if self.current_testcase:
            output_file = f"testcases/output_{self.current_testcase}.txt"
            if os.path.exists(output_file):
                os.remove(output_file)
                self.status_message = f"Output file for test case {self.current_testcase} removed!"
                self.status_message_color = DARK_GREEN
                self.load_solution()
            else:
                self.status_message = f"No output file exists for test case {self.current_testcase}."
                self.status_message_color = YELLOW

    
    
    def process_all_testcases(self):
        # Process all test cases sequentially
        all_performance_data = []
        
        for testcase_num in range(1, 7):  # 6 test cases from 1 to 6
            input_file = f"testcases/input_{testcase_num}.txt"
            output_file = f"testcases/output_{testcase_num}.txt"
            
            # Skip if output already exists
            if os.path.exists(output_file):
                continue
                
            # Skip if input doesn't exist
            if not os.path.exists(input_file):
                continue
                
            # Load the test case
            temp_grid = GameGrid.from_file(input_file)
            
            # Generate CNF
            encoder = CNFGenerator()
            encoder.generate_cnf(temp_grid)
            
            # Dictionary to store performance data for this testcase
            performance_data = {
                "test_case": testcase_num,  # Add test case number
                "PySAT": None,
                "Backtracking": None,
                "BruteForce": None
            }
            
            # Run solvers and get their execution times
            pysat = PySATSolver(temp_grid, encoder)
            pysat.get_solution() 
            performance_data["PySAT"] = pysat.execution_time * 1000  # Convert to ms
            pysat.save_solution(output_file, "PySAT", False)
            
            backtracking = BacktrackingSolver(temp_grid, encoder)
            backtracking.get_solution()  
            if backtracking.solution is None:
                performance_data["Backtracking"] = "N/A"
            else:
                performance_data["Backtracking"] = backtracking.execution_time * 1000  # Convert to ms
            backtracking.save_solution(output_file, "Backtracking", False)
            
            bf = BruteForceSolver(temp_grid, encoder)
            bf.get_solution()
            if bf.solution is None:
                performance_data["BruteForce"] = "N/A"
            else:
                performance_data["BruteForce"] = bf.execution_time * 1000  # Convert to ms
            bf.save_solution(output_file, "BruteForce", False)
            
            # Add to overall performance data
            all_performance_data.append(performance_data)
        
        # Save overall performance data (append mode)
        if all_performance_data:
            FileManager.save_performance("testcases/performance.txt", all_performance_data, append=True)
        
        # Update status message
        self.status_message = "All test cases processed!"
        self.status_message_color = DARK_GREEN
        
        # Reload current solution if a test case is selected
        if self.current_testcase:
            self.load_solution()

    def clear_all_output_files(self):
        # Clear all output files
        files_removed = 0
        for testcase_num in range(1, 7):  # 6 test cases from 1 to 6
            output_file = f"testcases/output_{testcase_num}.txt"
            if os.path.exists(output_file):
                os.remove(output_file)
                files_removed += 1
        
        performance_file = "testcases/performance.txt"
        if os.path.exists(performance_file):
            os.remove(performance_file)
            files_removed += 1
        # Update status message
        if files_removed > 0:
            self.status_message = f"{files_removed} output files removed!"
            self.status_message_color = DARK_GREEN
        else:
            self.status_message = "No output files to remove."
            self.status_message_color = YELLOW
        
        # Reload current solution
        if self.current_testcase:
            self.load_solution()


    def draw_section_borders(self):
        # Draw main section borders
        pygame.draw.line(self.screen, BLACK, (0, 140), (WINDOW_WIDTH, 140), 2)  # Top horizontal line
        pygame.draw.line(self.screen, BLACK, (650, 140), (650, WINDOW_HEIGHT), 2)  # Vertical divider
        
        # Draw section headers
        input_text = TITLE_FONT.render("Input Matrix", True, BLACK)
        self.screen.blit(input_text, (275, 155))
        
        solution_text = TITLE_FONT.render(f"Solution ({self.selected_algorithm})", True, BLACK)
        self.screen.blit(solution_text, (890, 155))

    def draw_input_grid(self):
        if not self.grid:
            return
        
        rows, cols = self.grid.rows, self.grid.cols
        max_size = max(rows, cols)
        
        # Calculate cell size based on grid dimensions
        cell_size = min(400 // max_size, 40)
        
        # Center the grid in the left section
        total_width = cols * cell_size
        total_height = rows * cell_size
        start_x = 75 + (500 - total_width) // 2
        start_y = 200 + (400 - total_height) // 2

        for row in range(rows):
            for col in range(cols):
                x = start_x + col * cell_size
                y = start_y + row * cell_size
                rect = pygame.Rect(x, y, cell_size, cell_size)
                
                # Draw cell
                pygame.draw.rect(self.screen, WHITE, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 1)
                
                # Draw cell content
                value = self.grid.data[row][col]
                if value != '_':
                    text = FONT.render(str(value), True, BLACK)
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)

    def draw_solution_grid(self):
        if not self.solution_grid:
            return
        
        self.solution_text = ""

        rows = len(self.solution_grid)
        cols = len(self.solution_grid[0]) if rows > 0 else 0
        max_size = max(rows, cols)
        
        # Calculate cell size based on grid dimensions
        cell_size = min(400 // max_size, 40)
        
        # Center the grid in the right section
        total_width = cols * cell_size
        total_height = rows * cell_size
        start_x = 725 + (500 - total_width) // 2
        start_y = 200 + (400 - total_height) // 2

        for row in range(rows):
            for col in range(cols):
                if col >= len(self.solution_grid[row]):
                    continue
                    
                x = start_x + col * cell_size
                y = start_y + row * cell_size
                rect = pygame.Rect(x, y, cell_size, cell_size)
                
                # Draw cell background based on content
                cell = self.solution_grid[row][col]
                if cell == 'T':  # Trap
                    pygame.draw.rect(self.screen, RED, rect)
                elif cell == 'G':  # Gem
                    pygame.draw.rect(self.screen, GREEN, rect)
                else:  # Number
                    pygame.draw.rect(self.screen, WHITE, rect)
                
                # Draw cell border
                pygame.draw.rect(self.screen, BLACK, rect, 1)
                
                # Draw cell content
                if cell != 'T' and cell != 'G':
                    text = FONT.render(cell, True, BLACK)
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)
                else:
                    # Draw letter T or G
                    text = FONT.render(cell, True, BLACK)
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)

    
    def draw_status_message(self):
        if self.status_message:
            text_surface = FONT.render(self.status_message, True, self.status_message_color)
            self.screen.blit(text_surface, (720, 90))

    def draw_solution_text(self):
        if self.solution_text:
            text_surface = TITLE_FONT.render(self.solution_text, True, BLACK)
            self.screen.blit(text_surface, (930, 350))

    def draw_legend(self):
        # Draw legend for colors
        legend_y = 650
        legend_x = 100
        text_x = 130
        legend_spacing = 120
        
        # Trap legend
        trap_rect = pygame.Rect(legend_x, legend_y, 20, 20)
        pygame.draw.rect(self.screen, RED, trap_rect)
        pygame.draw.rect(self.screen, BLACK, trap_rect, 1)
        text = SMALL_FONT.render("T - Trap", True, BLACK)
        self.screen.blit(text, (text_x, legend_y))
        
        # Gem legend
        gem_rect = pygame.Rect(legend_x + legend_spacing, legend_y, 20, 20)
        pygame.draw.rect(self.screen, GREEN, gem_rect)
        pygame.draw.rect(self.screen, BLACK, gem_rect, 1)
        text = SMALL_FONT.render("G - Gem", True, BLACK)
        self.screen.blit(text, (text_x + legend_spacing, legend_y))
        
        # Number legend
        num_rect = pygame.Rect(legend_x + 2*legend_spacing, legend_y, 20, 20)
        pygame.draw.rect(self.screen, WHITE, num_rect)
        pygame.draw.rect(self.screen, BLACK, num_rect, 1)
        text = SMALL_FONT.render("Number", True, BLACK)
        self.screen.blit(text, (text_x + 2*legend_spacing, legend_y))

    def run(self):
        running = True
        while running:
            self.screen.fill(LIGHT_GRAY)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Check testcase button clicks
                for i, button in enumerate(self.testcase_buttons):
                    if button.handle_event(event):
                        self.load_testcase(i + 1)
                
                # Check process button click
                if self.process_button.handle_event(event):
                    self.process_testcase()
                
                # Check open output button click
                if self.open_output_button.handle_event(event):
                    self.open_output_file()

                if self.clear_output_button.handle_event(event):
                    self.clear_output_file()

                if self.process_all_button.handle_event(event):
                    self.process_all_testcases()

                if self.clear_all_output_button.handle_event(event):
                    self.clear_all_output_files()
                
                # Check algorithm button clicks
                for button in self.algorithm_buttons:
                    if button.handle_event(event):
                        # Reset all buttons
                        for b in self.algorithm_buttons:
                            b.active = False
                        
                        # Set clicked button as active
                        button.active = True
                        
                        # Update selected algorithm
                        if button == self.pysat_button:
                            self.selected_algorithm = "PySAT"
                        elif button == self.backtracking_button:
                            self.selected_algorithm = "Backtracking"
                        elif button == self.bruteforce_button:
                            self.selected_algorithm = "BruteForce"
                        
                        # Load solution for the selected algorithm
                        self.load_solution()

            # Draw section borders
            self.draw_section_borders()
            
            # Draw grids and solution text
            self.draw_input_grid()
            self.draw_solution_grid()
            self.draw_solution_text()
            
            # Draw buttons
            for button in self.testcase_buttons:
                button.draw(self.screen)
            
            self.process_button.draw(self.screen)
            self.open_output_button.draw(self.screen)
            self.clear_output_button.draw(self.screen)
            self.process_all_button.draw(self.screen)
            self.clear_all_output_button.draw(self.screen)

            for button in self.algorithm_buttons:
                button.draw(self.screen)
            
            # Draw status message
            self.draw_status_message()
            
            # Draw legend
            self.draw_legend()
            
            pygame.display.flip()

        pygame.quit()
        sys.exit()