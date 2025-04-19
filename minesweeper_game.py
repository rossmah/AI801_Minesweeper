import random

class Minesweeper:
    def __init__(self, size=5, mines=5):
        self.size = size
        self.mines = mines
        self.first_move_made = False  # Ensures we place mines only after the first move
        self.board = [[' ' for _ in range(size)] for _ in range(size)]  # Hidden board
        self.visible_board = [['-' for _ in range(size)] for _ in range(size)]  # What the player sees
        self.mine_positions = set()  # Stores mine locations
        self.populate_mines()
        self.calculate_numbers()


def populate_mines(self, safe_zone=None):
    """Places mines randomly, avoiding the safe_zone (first move)."""
    safe_cells = set()
    if safe_zone:
        r, c = safe_zone
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
        safe_cells = {(r + dr, c + dc) for dr, dc in directions if 0 <= r + dr < self.size and 0 <= c + dc < self.size}

    self.mine_positions.clear()
    self.board = [[' ' for _ in range(self.size)] for _ in range(self.size)]  # Reset board

    while len(self.mine_positions) < self.mines:
        row, col = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
        if (row, col) not in self.mine_positions and (row, col) not in safe_cells:
            self.mine_positions.add((row, col))
            self.board[row][col] = 'M'

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
        if not self.first_move_made:
            self.populate_mines(safe_zone=(row, col))
            self.calculate_numbers()
            self.first_move_made = True

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

    def check_win(self):
        """Checks if the player has won (all non-mine cells revealed)."""
        revealed_cells = sum(row.count('-') for row in self.visible_board)
        return revealed_cells == self.mines
