# AI801_Minesweeper

# 1. Group Members:
Daryl Kwakye-Ackah (dpk5580@psu.edu) 
Holly Rossmann (har5412@psu.edu) 
Evan Turzanski (ert5255@psu.edu) 

## GitHub
This project is hosted publically on GitHib. To view, visit this link: https://github.com/rossmah/AI801_Minesweeper

# 2. Project Structure:
| File | Description |
| --- | --- |
`minesweeper.py` | Runs a regular version of the Minesweeper game that allows for human interaction and playthrough. Defaults to an 8x8 board with 10 mines.
`ai_agent.py` | Main file to run the AI agent and play a new game of Minesweeper. Defaults to an 8x8 board with 10 mines.
`run_x_times.py` | Runs multiple games using the AI agent to generate gameplay data.
`train_model.py`,` new_model.py` | Trains or updates a machine learning model based on logged game data.
`logger.py`, `data_preparation.py`, `analyze_data.py` | Supporting files for logging, data processing, and model inference.
`game_data.csv` | File where gameplay logs are saved for analysis and training.
`requirements.txt` | Contains necessary dependencies in order to run the python files

# 3. Requirements:
- Python 3.8 or newer
- Access to a terminal

# 4. Install Dependencies:
`pip3 install -r requirements.txt`

# 5. How to Run
There are two main ways to run the project's code. You may either use an executable (does not require dependencies), or you can run the python files directly.

## 5.1 Run Game using Executables
All executables can be found in the `dist` subdirectory. Once the project files have been downloaded, use a terminal to navigate to `AI801_MINESWEEPER/dist`. From there, run the commands below (instructions provided for a Mac. Terminal commands may vary slightly based on the operating system).

*As a note: Running the executable will cause the user to experience a delay in results being printed out. Be patient with the program as it runs, and it will display results after the entire code has been run.*

### Run Game using AI Agent
To run a single Minesweeper game that uses the AI Agent:
`./ai_agent`

### Run Game as a Human Player
To play a normal game of Minesweeper manually without AI assistance:
`./minesweeper`

## 5.2 Run Game using Python Files
### Run Game using AI Agent
To run a single Minesweeper game that uses the AI Agent:
`python3 ai_agent.py`

### Run Game as a Human Player
To play a normal game of Minesweeper manually without AI assistance:
`python3 minesweeper`

### Generate AI Gameplay Data (Multiple Games)
To run multiple AI games automatically to quickly populate the `game_data.csv` file:
`python3 run_x_times.py`

### Train or Update the Machine Learning Model
Once there is gameplay data populated in the CSV file, train the model by running:
`python3 train_model.py`