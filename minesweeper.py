import random

class Minesweeper:
    def __init__(self, size=8, mines=10):
        self.size = size  # Board size (NxN grid)
        self.mines = mines  # Number of mines
        self.board = [[' ' for _ in range(size)] for _ in range(size)]  # Hidden board
        self.visible_board = [['-' for _ in range(size)] for _ in range(size)]  # What the player sees
        self.mine_positions = set()  # Stores mine locations
        self.first_move_made = False # Track if first move has been made
        self.populate_mines()
        self.calculate_numbers()
        self.flags = set()

    '''
    Function: POPULATE_MINES
    Description: Randomly places mines on the board.
    '''
    def populate_mines(self):
        while len(self.mine_positions) < self.mines:
            row, col = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if (row, col) not in self.mine_positions:
                self.mine_positions.add((row, col))
                self.board[row][col] = 'M'  # 'M' represents a mine

    '''
    Function: CALCULATE_NUMBERS
    Description: Calculates numbers for non-mine cells based on adjacent mines.
    '''
    def calculate_numbers(self):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for row, col in self.mine_positions:
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc] != 'M':
                    if self.board[nr][nc] == ' ':
                        self.board[nr][nc] = 1
                    else:
                        self.board[nr][nc] += 1

    '''
    Function: GET_NEIGHBORS
    Description: Returns the valid neighboring cell positions around a given cell.
    '''
    def get_neighbors(self, row, col):
        directions = [(-1, -1), (-1, 0), (-1, 1),
                    (0, -1),         (0, 1),
                    (1, -1), (1, 0), (1, 1)]
        return [(row + dr, col + dc) for dr, dc in directions
                if 0 <= row + dr < self.size and 0 <= col + dc < self.size]

    '''
    Function: COUNT_FLAGS_NEARBY
    Description: Counts how many neighboring cells are flagged as mines.
    '''
    def count_flags_nearby(self, r, c):
        # Get the list of neighboring positions
        neighbors = self.get_neighbors(r, c)
        
        # Count how many of the neighbors are flagged
        flag_count = sum(1 for (nr, nc) in neighbors if self.visible_board[nr][nc] == 'F')  # 'F' represents a flagged cell
    
        return flag_count

    '''
    Function: RELOCATE_MINE
    Description: Moves a mine from a given cell (row, col) to a new random safe location and updates board numbers.
                 Only done if first move made is to reveal a tile that contains a mine. 
    '''
    def relocate_mine(self, row, col):
        self.mine_positions.remove((row, col))
        self.board[row][col] = ' '
        
        while True:
            new_row, new_col = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if (new_row, new_col) not in self.mine_positions and (new_row, new_col) != (row, col):
                self.mine_positions.add((new_row, new_col))
                self.board[new_row][new_col] = 'M'
                break

        # After relocating, re-calculate numbers
        self.reset_numbers()

    '''
    Function: RESET_NUMBERS
    Description: Clears and recalculates number hints on the board after mines are adjusted.
                Moves a mine from a given cell (row, col) to a new random safe location and updates board numbers.
                Only done if first move made is to reveal a tile that contains a mine. 
    '''
    def reset_numbers(self):
        self.board = [[' ' if cell != 'M' else 'M' for cell in row] for row in self.board]
        self.calculate_numbers()

    '''
    Function: REVEAL_CELL
    Description: Reveals the selected cell; recursively reveals neighbors if empty; guaranteeing safe first move.
    '''
    def reveal_cell(self, row, col):
        if not self.first_move_made:
            if (row, col) in self.mine_positions:
                self.relocate_mine(row, col)
            self.first_move_made = True
        
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

    '''
    Function: FLAG_CELL
    Description: Flags a cell as suspected to contain a mine.
    '''
    def flag_cell(self, row, col):
        if self.visible_board[row][col] == '-':
            self.visible_board[row][col] = 'F'
            self.flags.add((row, col))  # Add flagged cell to the set

    '''
    Function: DISPLAY_BOARD
    Description: Prints the current visible board with formatted row and column headers.
    '''
    def display_board(self):
        # Column headers
        print("    " + " ".join(f"{i:^3}" for i in range(self.size)))
        print("  " + "-" * (self.size * 4 ))

        for i, row in enumerate(self.visible_board):
            row_str = f"{i} |"
            for cell in row:
                # Center each cell in a 3-character space
                row_str += f" {cell:^3}"
            print(row_str)

    '''
    Function: CHECK_WIN
    Description: Checks if all non-mine cells are revealed and all mines are correctly flagged.
    '''
    def check_win(self):
        revealed_cells = 0
        flagged_mines = 0
        total_cells = self.size * self.size
        
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] != 'M':  # If it's not a mine
                    if self.visible_board[r][c] != '-':  # It's revealed
                        revealed_cells += 1
                if self.visible_board[r][c] == 'F' and self.board[r][c] == 'M':  # It's flagged and it's a mine
                    flagged_mines += 1
        
        # If all non-mine cells are revealed and all mines are flagged, the player wins
        if revealed_cells == (total_cells - self.mines) and flagged_mines == self.mines:
            return True
        
        return False
       
    '''
    Function: DISPLAY_MENU
    Description: Displays the welcome screen and instructions before the game starts.
    '''
    def display_menu(self):
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

    '''
    Function: PLAY
    Description: Main game loop that handles user input and game logic until win or loss.
    '''
    def play(self):
        self.display_menu()
        while True:
            self.display_board()

            if self.check_win():
                print("Congratulations! You won!")
                break

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
            
if __name__ == "__main__":
    game = Minesweeper(size=8, mines=10)
    game.play()
