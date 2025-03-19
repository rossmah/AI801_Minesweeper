import random

class Minesweeper:
    def __init__(self, size=5, mines=5):
        self.size = size  # Board size (NxN grid)
        self.mines = mines  # Number of mines
        self.board = [[' ' for _ in range(size)] for _ in range(size)]  # Hidden board
        self.visible_board = [['-' for _ in range(size)] for _ in range(size)]  # What the player sees
        self.mine_positions = set()  # Stores mine locations
        self.populate_mines()
        self.calculate_numbers()

    def populate_mines(self):
        """Randomly places mines on the board."""
        while len(self.mine_positions) < self.mines:
            row, col = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if (row, col) not in self.mine_positions:
                self.mine_positions.add((row, col))
                self.board[row][col] = 'M'  # 'M' represents a mine

    def calculate_numbers(self):
        """Calculates numbers for non-mine cells based on adjacent mines."""
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for row, col in self.mine_positions:
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc] != 'M':
                    if self.board[nr][nc] == ' ':
                        self.board[nr][nc] = 1
                    else:
                        self.board[nr][nc] += 1

    def reveal_cell(self, row, col):
        """Reveals a cell and expands empty areas recursively."""
        if (row, col) in self.mine_positions:
            return False  # Stepped on a mine, game over
        
        self.visible_board[row][col] = f'({self.board[row][col]})' if self.board[row][col] != ' ' else '(0)'
        
        if self.board[row][col] == ' ':
            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.size and 0 <= nc < self.size and self.visible_board[nr][nc] == '-':
                    self.reveal_cell(nr, nc)
        return True

    def flag_cell(self, row, col):
        """Flags a cell as a potential mine."""
        if self.visible_board[row][col] == '-':
            self.visible_board[row][col] = 'F'

    def display_board(self):
        """Displays the player's board with row and column numbers for reference."""
        print("  " + " ".join(str(i) for i in range(self.size)))  # Column numbers
        print("  " + "-" * (self.size * 2 - 1))  # Separator line
        for i, row in enumerate(self.visible_board):
            print(f"{i} | " + " ".join(row))

    def check_win(self):
        """Checks if the player has won (all non-mine cells revealed)."""
        revealed_cells = sum(row.count('-') for row in self.visible_board)
        return revealed_cells == self.mines

    def display_menu(self):
        """Displays the game menu with ASCII art and instructions."""
        print("""
        ==============================
        WELCOME TO MINESWEEPER
        ==============================
        Rules:
        - The board contains hidden mines.
        - Numbers indicate how many mines are adjacent.
        - Reveal a cell by entering 'r row col'.
        - Flag a suspected mine with 'f row col'.
        - Win by revealing all non-mine cells.
        - Lose if you reveal a mine!
        """)
        input("Press Enter to start...")

    def play(self):
        """Runs the game loop."""
        self.display_menu()
        while True:
            self.display_board()
            action = input("Enter 'r' to reveal or 'f' to flag (e.g., r 1 2): ").split()
            if len(action) != 3:
                print("Invalid input. Use format: r/f row col")
                continue

            cmd, row, col = action[0], int(action[1]), int(action[2])
            if cmd == 'r':
                if not self.reveal_cell(row, col):
                    print("Game Over! You hit a mine.")
                    break
            elif cmd == 'f':
                self.flag_cell(row, col)
            else:
                print("Invalid command.")
                continue
            
            if self.check_win():
                print("Congratulations! You won!")
                break

if __name__ == "__main__":
    game = Minesweeper(size=5, mines=5)
    game.play()
