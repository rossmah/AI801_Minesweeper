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

    '''
    Function: LOG_MOVE()
    Description: Logs a move during the game
    '''
    def log_move(self, game_id, move_number, row, col, action, board_state, mines_flagged, hidden_cells, safe, game_outcome):
        with open(self.file_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                game_id, move_number, row, col, action, board_state,
                mines_flagged, hidden_cells, safe, game_outcome
            ])

    '''
    Function: LOG_GAME_END()
    Description: Logs the outcome of a finished game.
    '''
    def log_game_end(self, game_id, outcome):
        with open(self.file_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([game_id, "End", "", "", "", "", "", "", "", outcome])
