import random
from collections import defaultdict
from minesweeper import Minesweeper

class AIAgent:
    def __init__(self, game):
        self.game = game
        self.size = game.size
        self.moves_made = set()
        self.flags = set()

    def get_neighbors(self, row, col):
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),         (0, 1),
                      (1, -1), (1, 0), (1, 1)]
        return [(row + dr, col + dc) for dr, dc in directions
                if 0 <= row + dr < self.size and 0 <= col + dc < self.size]

    def apply_heuristics(self):
        safe_moves = set()
        mine_guesses = set()

        for r in range(self.size):
            for c in range(self.size):
                cell = self.game.visible_board[r][c]
                if cell.startswith("(") and cell.endswith(")"):
                    number = int(cell.strip("()"))
                    neighbors = self.get_neighbors(r, c)
                    hidden = [n for n in neighbors if self.game.visible_board[n[0]][n[1]] == '-']
                    flagged = [n for n in neighbors if self.game.visible_board[n[0]][n[1]] == 'F']

                    if number == len(flagged) + len(hidden):
                        mine_guesses.update(hidden)
                    elif number == len(flagged):
                        safe_moves.update(hidden)

        return safe_moves, mine_guesses

    def monte_carlo_guess(self, trials=100):
        counts = defaultdict(int)

        for _ in range(trials):
            simulated_flags = set()
            for r in range(self.size):
                for c in range(self.size):
                    if self.game.visible_board[r][c] == '-' and random.random() < 0.15:
                        simulated_flags.add((r, c))

            for r in range(self.size):
                for c in range(self.size):
                    if (r, c) in simulated_flags:
                        counts[(r, c)] += 1

        sorted_cells = sorted(counts.items(), key=lambda item: item[1])
        for cell, _ in sorted_cells:
            if cell not in self.moves_made:
                return cell
        return None

    def get_next_move(self):
        safe_moves, mine_guesses = self.apply_heuristics()

        for move in safe_moves:
            if move not in self.moves_made:
                return ('r', *move)

        for move in mine_guesses:
            if move not in self.flags:
                self.flags.add(move)
                return ('f', *move)

        guess = self.monte_carlo_guess()
        if guess:
            return ('r', *guess)

        # Fallback to random
        while True:
            row, col = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if (row, col) not in self.moves_made and self.game.visible_board[row][col] == '-':
                return ('r', row, col)

    def play(self):
        print("AI is playing Minesweeper...\n")
        self.game.display_board()

        while True:
            move = self.get_next_move()
            self.moves_made.add((move[1], move[2]))
            print(f"\nAI Move: {move}")

            if move[0] == 'r':
                alive = self.game.reveal_cell(move[1], move[2])
                if not alive:
                    print("\nAI hit a mine. Game Over!")
                    self.game.display_board()
                    break
            elif move[0] == 'f':
                self.game.flag_cell(move[1], move[2])

            if self.game.check_win():
                print("\nAI Wins!")
                self.game.display_board()
                break

            self.game.display_board()

# Run the AI
if __name__ == "__main__":
    game = Minesweeper(size=5, mines=5)
    ai = AIAgent(game)
    ai.play()
