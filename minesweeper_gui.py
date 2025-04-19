import pygame
import random
from minesweeper_game import Minesweeper
from sprite_manager import SpriteManager



# Constants for screen size and tile size
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TILE_SIZE = 32

# Define the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Pygame constants
WIDTH = 500
HEIGHT = 500
CELL_SIZE = 50


class MinesweeperGUI:
    def __init__(self, game, window_size=(500, 500)):
        pygame.init()  # Initialize pygame

        self.game = game
        self.window_size = window_size
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Minesweeper")
        
        self.sprite_manager = SpriteManager('spritesheet.png')
        
        # Calculate the size of each square based on the window size
        #self.square_size = min(self.window_size[0] // self.game.size, self.window_size[1] // self.game.size)
        self.square_size = min(self.window_size[0] // (self.game.size * 2), self.window_size[1] // (self.game.size * 2))
        print(f"Calculated square size: {self.square_size}")


        

    def draw_board(self):
        """Draws the entire game board."""
        self.screen.blit(self.sprite_manager.get_sprite(0, 0, self.square_size), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))


        for row in range(self.game.size):
            for col in range(self.game.size):
                self.draw_square(row, col)


    def draw_square(self, row, col):
        """Draws a single square, either revealed or hidden."""
        x = col * self.square_size
        y = row * self.square_size
        
        cell = self.game.visible_board[row][col]
        
        # Set background color based on the cell type (adjust as needed)
        if cell == '-':
            color = (192, 192, 192)  # Default background color for hidden cells
        elif cell == 'F':
            color = (255, 0, 0)  # Red for flagged cells (this can be adjusted)
        else:
            color = (255, 255, 255)  # White for revealed cells
        
        # Fill the cell background
        pygame.draw.rect(self.screen, color, (x, y, self.square_size, self.square_size))
        
        # Draw the appropriate sprite for this cell
        if cell == 'F':
            self.screen.blit(self.sprite_manager.get_sprite(0, 2, self.square_size), (x, y))  # Flag sprite
        elif cell == 'M':
            self.screen.blit(self.sprite_manager.get_sprite(0, 0, self.square_size), (x, y))  # Mine with grey background
        elif cell == '0':
            self.screen.blit(self.sprite_manager.get_sprite(1, 1, self.square_size), (x, y))  # Blank clicked tile
        elif isinstance(cell, int):
            sprite = self.sprite_manager.get_sprite(cell - 1, 0, self.square_size)  # Numbered block
            self.screen.blit(sprite, (x, y))





    def run(self):
        """Main game loop."""
        running = True
        while running:
            self.screen.fill((255, 255, 255))  # Fill background with white color
            self.draw_board()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    col = event.pos[0] // self.square_size
                    row = event.pos[1] // self.square_size
                    self.game.reveal_cell(row, col)
                
            pygame.display.flip()
            pygame.time.Clock().tick(60)  # 60 FPS

        pygame.quit()

if __name__ == "__main__":
    try:
        # Instantiate the game with 5x5 grid and 5 mines
        game = Minesweeper(size=5, mines=5)
        # Instantiate the GUI with the created game
        gui = MinesweeperGUI(game)
        # Run the game (start the game loop)
        gui.run()
    except Exception as e:
        # Catch and print any exceptions
        print(f"Error: {e}")
