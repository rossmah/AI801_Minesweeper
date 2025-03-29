import random
from minesweeper import Minesweeper

class SimpleAIAgent:
    def __init__(self, game):
        self.game = game
        self.size = game.size
        self.known_safe = set()
        self.known_mines = set()
        self.moves_made = set()

    def get_next_move(self):
        # First try: any known safe cell
        for r in range(self.size):
            for c in range(self.size):
                if (r, c) not in self.moves_made and self.game.visible_board[r][c] == '-' and (r, c) not in self.known_mines:
                    return ('r', r, c)

        # Otherwise, guess randomly
        while True:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            if (row, col) not in self.moves_made and self.game.visible_board[row][col] == '-':
                return ('r', row, col)

    def play(self):
        print("AI playing Minesweeper...\n")
        self.game.display_board()

        while True:
            move = self.get_next_move()
            self.moves_made.add((move[1], move[2]))
            print(f"\nAI Move: {move}")
            
            if move[0] == 'r':
                alive = self.game.reveal_cell(move[1], move[2])
                if not alive:
                    print("\nAI hit a mine. Game over!")
                    self.game.display_board()
                    break
            elif move[0] == 'f':
                self.game.flag_cell(move[1], move[2])

            if self.game.check_win():
                print("\nAI wins!")
                self.game.display_board()
                break

            self.game.display_board()


# Run the AI agent
if __name__ == "__main__":
    game = Minesweeper(size=5, mines=5)
    ai = SimpleAIAgent(game)
    ai.play()
