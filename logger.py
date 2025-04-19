import csv
import os

class GameLogger:
    def __init__(self, file_name="game_data.csv"):
        self.file_name = file_name
        # Check if the file already exists; if not, create it and write headers
        if not os.path.exists(self.file_name):
            with open(self.file_name, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Game ID", "Move Number", "Row", "Col", "Action", "Board State",
                    "Mines Flagged", "Hidden Cells", "Safe", "Game Outcome"
                ])

    def log_move(self, game_id, move_number, row, col, action, board_state, mines_flagged, hidden_cells, safe, game_outcome):
        """Logs a move during the game."""
        with open(self.file_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                game_id, move_number, row, col, action, board_state,
                mines_flagged, hidden_cells, safe, game_outcome
            ])

    def log_game_end(self, game_id, outcome):
        """Logs the outcome of a finished game."""
        with open(self.file_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([game_id, "End", "", "", "", "", "", "", "", outcome])
