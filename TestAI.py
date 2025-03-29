import random
from collections import defaultdict
from minesweeper import Minesweeper

class BayesianAIAgent:
    def __init__(self, game):
        self.game = game
        self.size = game.size
        self.moves_made = set()
        self.flagged_mines = set()
        self.safe_cells = set()
        self.cell_probabilities = {}
        self.learning_rate = 0.1  # How quickly to adjust probabilities after mistakes
        self.mine_patterns = defaultdict(int)  # Track patterns that led to mines
        
        # Initialize probabilities
        for r in range(self.size):
            for c in range(self.size):
                self.cell_probabilities[(r, c)] = game.mines / (self.size * self.size)
    
    def update_probabilities(self):
        """Update probabilities based on current board state"""
        # Reset probabilities for known cells
        for r in range(self.size):
            for c in range(self.size):
                if (r, c) in self.flagged_mines:
                    self.cell_probabilities[(r, c)] = 1.0
                elif (r, c) in self.safe_cells:
                    self.cell_probabilities[(r, c)] = 0.0
        
        # For each revealed number, adjust probabilities of neighbors
        for r in range(self.size):
            for c in range(self.size):
                if isinstance(self.game.visible_board[r][c], int):
                    hidden_neighbors = []
                    flagged_neighbors = 0
                    
                    # Get all neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < self.size and 0 <= nc < self.size:
                                if (nr, nc) in self.flagged_mines:
                                    flagged_neighbors += 1
                                elif self.game.visible_board[nr][nc] == '-':
                                    hidden_neighbors.append((nr, nc))
                    
                    # Calculate remaining mines
                    remaining_mines = self.game.visible_board[r][c] - flagged_neighbors
                    if remaining_mines > 0 and hidden_neighbors:
                        prob = remaining_mines / len(hidden_neighbors)
                        for cell in hidden_neighbors:
                            # Bayesian update: combine prior with new evidence
                            prior = self.cell_probabilities[cell]
                            self.cell_probabilities[cell] = prior * prob / (prior * prob + (1 - prior) * (1 - prob))
    
    def learn_from_mistake(self, cell):
        """Adjust probabilities based on hitting a mine"""
        # Store the pattern around the mine
        pattern = self.get_cell_pattern(cell)
        self.mine_patterns[pattern] += 1
        
        # Reduce probability of similar cells in the future
        for r in range(self.size):
            for c in range(self.size):
                if (r, c) not in self.moves_made and self.game.visible_board[r][c] == '-':
                    similarity = self.pattern_similarity(pattern, self.get_cell_pattern((r, c)))
                    self.cell_probabilities[(r, c)] = min(1.0, 
                        self.cell_probabilities[(r, c)] + self.learning_rate * similarity)
    
    def get_cell_pattern(self, cell):
        """Get a pattern descriptor for the cell's neighborhood"""
        r, c = cell
        pattern = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    val = self.game.visible_board[nr][nc]
                    pattern.append('M' if (nr, nc) in self.flagged_mines else 
                                   'N' if isinstance(val, int) else 'U')
                else:
                    pattern.append('X')  # Edge
        return tuple(pattern)
    
    def pattern_similarity(self, pattern1, pattern2):
        """Calculate similarity between two patterns"""
        matches = sum(1 for p1, p2 in zip(pattern1, pattern2) if p1 == p2 and p1 != 'X')
        return matches / len(pattern1)
    
    def get_next_move(self):
        self.update_probabilities()
        
        # First, look for guaranteed safe moves
        safe_moves = [cell for cell, prob in self.cell_probabilities.items()
                     if prob == 0 and cell not in self.moves_made and cell not in self.flagged_mines]
        if safe_moves:
            return ('r', *min(safe_moves))  # Return first safe move (could use more sophisticated selection)
        
        # Then look for guaranteed mines
        mine_moves = [cell for cell, prob in self.cell_probabilities.items()
                     if prob == 1 and cell not in self.flagged_mines]
        if mine_moves:
            return ('f', *min(mine_moves))
        
        # If no certain moves, choose the safest available
        possible_moves = [(cell, prob) for cell, prob in self.cell_probabilities.items()
                         if cell not in self.moves_made and cell not in self.flagged_mines
                         and self.game.visible_board[cell[0]][cell[1]] == '-']
        
        if not possible_moves:
            return None  # No moves left
        
        # Choose the cell with lowest mine probability
        safest_move = min(possible_moves, key=lambda x: x[1])
        return ('r', *safest_move[0])
    
    def play(self):
        print("Bayesian AI playing Minesweeper...\n")
        self.game.display_board()

        while True:
            move = self.get_next_move()
            if not move:
                print("\nNo valid moves left!")
                break
                
            self.moves_made.add((move[1], move[2]))
            print(f"\nAI Move: {move}")
            print(f"Estimated mine probability: {self.cell_probabilities[(move[1], move[2])]:.2f}")

            if move[0] == 'r':
                alive = self.game.reveal_cell(move[1], move[2])
                if alive:
                    self.safe_cells.add((move[1], move[2]))
                else:
                    self.learn_from_mistake((move[1], move[2]))
                    print("\nAI hit a mine. Game over!")
                    self.game.display_board()
                    break
            elif move[0] == 'f':
                self.flagged_mines.add((move[1], move[2]))
                self.game.flag_cell(move[1], move[2])

            if self.game.check_win():
                print("\nAI wins!")
                self.game.display_board()
                break

            self.game.display_board()


# Run the AI agent
if __name__ == "__main__":
    game = Minesweeper(size=5, mines=5)
    ai = BayesianAIAgent(game)
    ai.play()
