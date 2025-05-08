import pygame
import sys
import os
from game_grid import GameGrid
from bruteforce_solver import BruteForceSolver
from cnf_generate import CNFGenerator
from pysat_solver import PySATSolver
# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Font
FONT = pygame.font.SysFont('Roboto', 24)
SMALL_FONT = pygame.font.SysFont('Roboto', 18)

class Button:
    def __init__(self, x, y, width, height, text, color=GRAY):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.is_hovered = False

    def draw(self, screen):
        color = (min(self.color[0] + 30, 255), min(self.color[1] + 30, 255), min(self.color[2] + 30, 255)) if self.is_hovered else self.color
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
        
        # Create buttons
        button_width = 200
        button_height = 50
        spacing = 200
        
        self.testcase_buttons = [
            Button(50 + i * (button_height + spacing), 20,
                  button_width, button_height, 
                  f"Test Case {i+1}")
            for i in range(3)
        ]
        
        self.process_button = Button(50, 90, button_width, button_height, "Process", GREEN)
        self.open_output_button = Button(300, 90, button_width, button_height, "Open Output", BLUE)
        
        self.current_testcase = None
        self.grid = None
        self.output_text = ""

    def load_testcase(self, testcase_num):
        input_file = f"./testcases/input_{testcase_num}.txt"
        if os.path.exists(input_file):
            self.grid = GameGrid.from_file(input_file)
            self.current_testcase = testcase_num
            self.output_text = ""

    def process_testcase(self):
        if self.grid and self.current_testcase:
            encoder = CNFGenerator()
            encoder.generate_constraints(self.grid)
            
            bf = BruteForceSolver(self.grid, encoder)
            pysat = PySATSolver(self.grid, encoder)

            output_file = f"./testcases/output_{self.current_testcase}.txt"
            bf.save_solution(output_file, "BruteForce", False)
            pysat.save_solution(output_file, "PySAT", False)
            

            # if self.solution:
            #     output_file = f"./testcases/output_{self.current_testcase}.txt"
            #     solver.save_solution(output_file, "BruteForce", False)
            #     self.output_text = "Đã xử lý xong và lưu kết quả!"
            # else:
            #     self.output_text = "Không tìm thấy giải pháp!"

    def open_output_file(self):
        if self.current_testcase:
            print(self.current_testcase)
            output_file = f"./testcases/output_{self.current_testcase}.txt"
            if os.path.exists(output_file):
                os.startfile(output_file)

    def draw_grid(self):
        if not self.grid:
            return

        cell_size = 20
        start_x = 50
        start_y = 200

        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
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

    def draw_solution(self):

        cell_size = 20
        start_x = 700
        start_y = 50

        # for var_id in self.solution:
        #     if var_id > 0:  # Only show positive variables (traps)
        #         pos = self.grid.encoder.get_position(var_id)
        #         if pos:
        #             row, col = pos
        #             x = start_x + col * cell_size
        #             y = start_y + row * cell_size
        #             rect = pygame.Rect(x, y, cell_size, cell_size)
        #             pygame.draw.rect(self.screen, RED, rect)
        #             pygame.draw.rect(self.screen, BLACK, rect, 1)

    def run(self):
        running = True
        while running:
            self.screen.fill(WHITE)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Check button clicks
                for i, button in enumerate(self.testcase_buttons):
                    if button.handle_event(event):
                        self.load_testcase(i + 1)
                
                if self.process_button.handle_event(event):
                    self.process_testcase()
                
                if self.open_output_button.handle_event(event):
                    self.open_output_file()

            # Draw buttons
            for button in self.testcase_buttons:
                button.draw(self.screen)
            self.process_button.draw(self.screen)
            self.open_output_button.draw(self.screen)

            # Draw grid and solution
            self.draw_grid()
            self.draw_solution()

            # Draw output text
            if self.output_text:
                text_surface = FONT.render(self.output_text, True, BLACK)
                self.screen.blit(text_surface, (50, 400))

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    gui = GameGUI()
    gui.run() 