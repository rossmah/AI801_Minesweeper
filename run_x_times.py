import subprocess

# Initialize the logger
logfile = "game_data.csv"

# Run ai_agent.py 50 times without displaying output
for x in range(50):
    subprocess.run(["python3", "ai_agent.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Run: ", x, " Complete.")
