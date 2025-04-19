import random
from collections import defaultdict
from minesweeper import Minesweeper
from logger import GameLogger
import pickle
import os

class AIAgent:
    def __init__(self, game, logger=None): 
        self.game = game
        self.size = game.size
        self.moves_made = set()
        self.flags = set()
        self.logger = logger if logger else GameLogger() 
        self.model = None

        model_path = 'models/minesweeper_model.pkl'
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
        else:
            print("Warning: Trained model not found. ML-based prediction will be disabled.")

    def load_model(filename="minesweeper_model.pkl"):
        """Load the trained model from a file."""
        try:
            with open(filename, 'rb') as file:
                model = pickle.load(file)
            print(f"Model loaded from {filename}")
            return model
        except FileNotFoundError:
            print(f"Model file {filename} not found. Proceeding with untrained model.")
            return None  # Return None or a default model if not found

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

    def minimum_risk_guess(self):
        '''
        This function is used when no safe moves or obvious mines can be found using heuristics.
        It estimates the risk for each unknown cell based on nearby revealed numbers and selects
        the cell with the lowest probability of being a mine.
        '''

        risk_map = {}
        
        for r in range(self.size):
            for c in range(self.size):
                cell = self.game.visible_board[r][c]
                
                # Only consider revealed number cells
                if cell.startswith("(") and cell.endswith(")"):
                    number = int(cell.strip("()"))
                    neighbors = self.get_neighbors(r, c)
                    
                    # Count hidden and flagged neighbors
                    hidden = [n for n in neighbors if self.game.visible_board[n[0]][n[1]] == '-']
                    flagged = [n for n in neighbors if self.game.visible_board[n[0]][n[1]] == 'F']
                    
                    mines_left = number - len(flagged)
                    
                    # Assign estimated risk to hidden neighbors
                    if hidden and mines_left >= 0:
                        risk = mines_left / len(hidden)
                        for cell_pos in hidden:
                            if cell_pos in risk_map:
                                risk_map[cell_pos].append(risk)
                            else:
                                risk_map[cell_pos] = [risk]

        # Average the risk from all sources for each cell
        avg_risk_map = {cell: sum(risks)/len(risks) for cell, risks in risk_map.items()}

        # Select the lowest-risk cell that hasn't been played
        if avg_risk_map:
            best_cell = min(avg_risk_map.items(), key=lambda x: x[1])[0]
            return best_cell

        # If no risk-based info is available, fallback to random
        for r in range(self.size):
            for c in range(self.size):
                if (r, c) not in self.moves_made and self.game.visible_board[r][c] == '-':
                    return (r, c)

    def predict_with_model(self):
        """
        Use the trained model to predict the safest move among all unrevealed cells.
        Returns the (row, col) of the best predicted move, or None if not enough data.
        """
        candidate_moves = []

        for r in range(self.height):
            for c in range(self.width):
                if (r, c) in self.moves_made or (r, c) in self.flags:
                    continue

                adjacent = self.count_adjacent_flags(r, c)
                is_revealed = int((r, c) in self.moves_made)
                is_flagged = int((r, c) in self.flags)
                is_mine = int((r, c) in self.mines)  # Optional; could default to 0
                norm_row = r / self.height
                norm_col = c / self.width

                features = [[adjacent, is_revealed, is_flagged, is_mine, norm_row, norm_col]]
                prediction = self.model.predict_proba(features)[0][0]  # Probability of being safe
                candidate_moves.append(((r, c), prediction))

        if candidate_moves:
            # Sort by highest predicted safety
            candidate_moves.sort(key=lambda x: x[1], reverse=True)
            return candidate_moves[0][0]
        return None

    
    def get_next_move(self):
        """
        Decide the next move using heuristics, minimum-risk analysis, or a trained ML model.
        Priority: 
        1. Obvious safe moves (heuristics)
        2. Obvious mines to flag (heuristics)
        3. Minimum-risk guess
        4. Model-based prediction (learned from historical data)
        5. Random fallback
        """
        safe_moves, mine_guesses = self.apply_heuristics()

        # Logging game state
        game_id = id(self.game)
        move_number = len(self.moves_made) + 1
        mines_flagged = len(self.flags)
        hidden_cells = sum(row.count('-') for row in self.game.visible_board)
        board_state = str(self.game.visible_board)
        safe = False
       #safe = move_number == 1  # First move is always safe

        if move_number == 1:  # First move should be safe
            self.moves_made.add((0, 0))  # Make sure to mark (0,0) as the first move
            self.logger.log_move(game_id, move_number, 0, 0, 'r', board_state, mines_flagged, hidden_cells, True, "Ongoing")
            return ('r', 0, 0)  # Force the first move to be (0,0)


        # Step 1: Obvious safe moves
        for move in safe_moves:
            if move not in self.moves_made:
                self.logger.log_move(game_id, move_number, move[0], move[1], 'r', board_state, mines_flagged, hidden_cells, safe, "Ongoing")
                return ('r', *move)

        # Step 2: Flag obvious mines
        for move in mine_guesses:
            if move not in self.flags:
                self.flags.add(move)
                self.logger.log_move(game_id, move_number, move[0], move[1], 'f', board_state, mines_flagged, hidden_cells, safe, "Ongoing")
                return ('f', *move)

        

        # Step 4: Use trained ML model to suggest next move
        if self.model:
            prediction = self.predict_with_model()
            if prediction:
                row, col = prediction
                self.logger.log_move(game_id, move_number, row, col, 'r', board_state, mines_flagged, hidden_cells, safe, "Ongoing")
                return ('r', row, col)
            '''   features = self.extract_features_for_model()
            predicted_move = self.model.predict([features])[0]  # Assumes model is sklearn-like
            if predicted_move and self.is_valid_guess(predicted_move):
                row, col = predicted_move
                self.logger.log_move(game_id, move_number, row, col, 'r', board_state, mines_flagged, hidden_cells, safe, "Ongoing")
                return ('r', row, col)'''

        # Step 3: Try minimum-risk guess
        guess = self.minimum_risk_guess()
        if guess:
            self.logger.log_move(game_id, move_number, guess[0], guess[1], 'r', board_state, mines_flagged, hidden_cells, safe, "Ongoing")
            return ('r', *guess)

        # Step 5: Fallback to random guess
        while True:
            row, col = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if (row, col) not in self.moves_made and self.game.visible_board[row][col] == '-':
                self.logger.log_move(game_id, move_number, row, col, 'r', board_state, mines_flagged, hidden_cells, safe, "Ongoing")
                return ('r', row, col)

     


    def play(self):
        print("AI is playing Minesweeper...\n")
        self.game.display_board()

        # Unique ID for the game session
        game_id = id(self.game)

        while True:
            move = self.get_next_move()
            self.moves_made.add((move[1], move[2]))
            print(f"\nAI Move: {move}")

            if move[0] == 'r':
                alive = self.game.reveal_cell(move[1], move[2])
                if not alive:
                    print("\nAI hit a mine. Game Over!")
                    self.game.display_board()
                    self.logger.log_game_end(game_id, "Loss")
                    break
            elif move[0] == 'f':
                self.game.flag_cell(move[1], move[2])

            if self.game.check_win():
                print("\nAI Wins!")
                self.game.display_board()
                self.logger.log_game_end(game_id, "Win")
                break

            self.game.display_board()

# Run the AI
if __name__ == "__main__":
    game = Minesweeper(size=5, mines=5)
    ai = AIAgent(game)
    ai.play()