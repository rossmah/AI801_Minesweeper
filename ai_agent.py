import random
import pickle
import os
import joblib
from collections import defaultdict
from minesweeper import Minesweeper
from logger import GameLogger
from sklearn.preprocessing import StandardScaler

class AIAgent:
    """
    Function: __init__
    Description: Initializes the AI agent with a Minesweeper game instance and optional logger.
    Loads the ML model and sets up internal state for tracking moves and flags.
    """
    def __init__(self, game, logger:GameLogger=None): 
        self.game = game
        self.size = game.size
        self.height = game.size
        self.width = game.size
        self.mines = getattr(game, 'mine_positions', set())
        self.moves_made = set()
        self.flags = set()
        self.logger = logger if logger else GameLogger() 
        self.scaler = StandardScaler()
        self.model = None
        self.load_model()

    """
    Function: LOAD_MODEL()
    Description: Attempts to load a previously trained ML model and scaler from disk.
    If unavailable, sets them to None.
    """
    def load_model(self):
        try:
            # Try loading the model and scaler
            self.model = joblib.load('model.pkl')
            self.scaler = joblib.load('scaler.pkl')
           # self.scaler.fit(data)  # Fit the scaler with training data
        except:
            # If not found, set them to None
            self.model = None
            self.scaler = None
    
    """
    Function: PREPARE_DATA()
    Description: Reads game data from a CSV file and prepares it for model training.
    Returns extracted features for learning.
    """
    def prepare_data(self):
        # Read the game data from CSV
        game_data = pd.read_csv(self.game_data_file)
        features = prepare_data(game_data)
        return features

    """
    Function: RETRAIN_MODEL()
    Description: Retrains the ML model using newly prepared data.
    Initializes model and scaler if not previously loaded.
    Saves the updated model and scaler to disk.
    """
    def retrain_model(self):
        # Prepare the data
        features = self.prepare_data()
        
        # If no model or scaler exists, initialize them
        if self.model is None or self.scaler is None:
            self.scaler = StandardScaler()
            self.model = train_model(features, self.scaler)
        
        # Otherwise, just retrain the model
        else:
            self.model = train_model(features, self.scaler)
        
        # Save the model and scaler for future use
        joblib.dump(self.model, 'model.pkl')
        joblib.dump(self.scaler, 'scaler.pkl')

    """
    Function: APPLY_HEURISTICS()
    Description: Applies basic Minesweeper heuristics to identify safe moves and likely mines.
    Returns two sets: one of safe moves and one of suspected mine locations.
    """
    def apply_heuristics(self):
        safe_moves = set()
        mine_guesses = set()

        for r in range(self.size):
            for c in range(self.size):
                cell = self.game.visible_board[r][c]
                if cell.startswith("(") and cell.endswith(")"):
                    number = int(cell.strip("()"))
                    neighbors = self.game.get_neighbors(r, c)
                    hidden = [n for n in neighbors if self.game.visible_board[n[0]][n[1]] == '-']
                    flagged = [n for n in neighbors if self.game.visible_board[n[0]][n[1]] == 'F']

                    if number == len(flagged) + len(hidden):
                        mine_guesses.update(hidden)
                    elif number == len(flagged):
                        safe_moves.update(hidden)

        return safe_moves, mine_guesses

    """
    Function: MONTE_CARLO_GUESS
    Description: Performs a simple Monte Carlo simulation to estimate likely mine positions.
    Returns the cell with the lowest simulated mine probability not yet played.
    """
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

    '''
    Function: MINIMUM_RISK_GUESS()
    Definition: This function is used when no safe moves or obvious mines can be found using heuristics.
    It estimates the risk for each unknown cell based on nearby revealed numbers and selects
    the cell with the lowest probability of being a mine.
    '''
    def minimum_risk_guess(self):
        risk_map = {}
        
        for r in range(self.size):
            for c in range(self.size):
                cell = self.game.visible_board[r][c]
                
                # Only consider revealed number cells
                if cell.startswith("(") and cell.endswith(")"):
                    number = int(cell.strip("()"))
                    neighbors = self.game.get_neighbors(r, c)
                    
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

    """
    Function: PREDICT_WITH_MODEL()
    Definition: Use the trained model to predict the safest move among all unrevealed cells.
    Returns the (row, col) of the best predicted move, or None if not enough data.
    """
    def predict_with_model(self):
        if not self.model or not self.scaler:
            raise ValueError("Model or scaler is not loaded.")

        candidate_moves = []
        #self.scaler.fit(data)  # Fit the scaler with training data

        try: 
            for r in range(self.height):
                for c in range(self.width):
                    if (r, c) in self.moves_made or (r, c) in self.flags:
                        continue

                    # Basic features
                    mines_flagged = self.game.count_flags_nearby(r, c)
                    hidden_cells_count = sum(1 for cell in self.game.get_neighbors(r, c) if cell == '-')

                    features = [[r, c, mines_flagged, hidden_cells_count]]
                    features_scaled = self.scaler.transform(features)

                    prob_safe = self.model.predict_proba(features_scaled)[0][1]

                    candidate_moves.append(((r, c), prob_safe))

            if candidate_moves:
                best_move = max(candidate_moves, key=lambda x: x[1])[0]
                return best_move
        except Exception as e:
            print(f"Prediction failed: {e}")
            return None
    
    """
    Functions: GET_NEXT_MOVE()
    Description: Decide the next move using heuristics, minimum-risk analysis, or a trained ML model.
        Priority: 
        1. Obvious safe moves (heuristics)
        2. Obvious mines to flag (heuristics)
        3. Minimum-risk guess
        4. Model-based prediction (learned from historical data)
        5. Random fallback
    """
    def get_next_move(self):
        # Logging game state
        game_id = id(self.game)
        move_number = len(self.moves_made) + 1
        mines_flagged = len(self.flags)
        hidden_cells = sum(row.count('-') for row in self.game.visible_board)
        board_state = str(self.game.visible_board)
        safe = True

        # Retrieve safe moves and mine guesses from heuristics
        safe_moves, mine_guesses = self.apply_heuristics()

        # Step 1: Obvious safe moves (Heuristics)
        for move in safe_moves:
            if move not in self.moves_made:
                # Reveal the move
                alive = self.game.reveal_cell(move[0], move[1])
                if not alive:
                    safe = False  
                self.logger.log_move(game_id, move_number, move[0], move[1], 'r', board_state, mines_flagged, hidden_cells, safe, "Ongoing")
                return ('r', *move)

        
        # Step 2: Flag obvious mines (Heuristics)
        for move in mine_guesses:
            if move not in self.flags:
                self.flags.add(move)
                safe = True
                self.logger.log_move(game_id, move_number, move[0], move[1], 'f', board_state, mines_flagged, hidden_cells, safe, "Ongoing")
                return ('f', *move)

        # Step 3: Use trained ML model to suggest next move
        if self.model and self.scaler:
            print("TRYING TO PREDICT WITH MODEL")
            prediction = self.predict_with_model()
            if prediction:
                safe = True
                row, col = prediction
                self.logger.log_move(game_id, move_number, row, col, 'r', board_state, mines_flagged, hidden_cells, safe, "Ongoing")
                return ('r', row, col)
        
        # Step 4: Try minimum-risk guess
        guess = self.minimum_risk_guess()
        if guess:
            safe = True
            self.logger.log_move(game_id, move_number, guess[0], guess[1], 'r', board_state, mines_flagged, hidden_cells, safe, "Ongoing")
            return ('r', *guess)
        
        # Step 5. If model doesn't predict, use Monte Carlo guess
        guess = self.monte_carlo_guess()
        if guess:
            safe = True
            self.logger.log_move(game_id, move_number, guess[0], guess[1], 'r', board_state, mines_flagged, hidden_cells, safe, "Ongoing")
            return ('r', *guess)
        
        # Step 6: Fallback to random guess
        while True:
            row, col = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if (row, col) not in self.moves_made and self.game.visible_board[row][col] == '-':
                safe = True
                self.logger.log_move(game_id, move_number, row, col, 'r', board_state, mines_flagged, hidden_cells, safe, "Ongoing")
                return ('r', row, col)
        
    """
    Function: PLAY()
    Description: Run the game loop for the AI agent until the game ends.
    The agent continually chooses the next move using its strategy (heuristics, ML model,
    or probabilistic guessing) and performs the move on the Minesweeper board.
    Game state is updated after each move, and the loop exits when the game is won or lost.
    """
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

    """
    Function: __main__
    Description: Entry point for running the Minesweeper AI agent.
    Initializes the game and AI agent, then starts the game loop by calling play().
    Used for standalone execution of the AI agent to play a full game.
    """
if __name__ == "__main__":
    # Run the AI
    game = Minesweeper(size=8, mines=10)
    ai = AIAgent(game)
    ai.play()