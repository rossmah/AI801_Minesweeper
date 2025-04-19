import subprocess

# Run ai_agent.py 100 times without displaying output
for _ in range(100):
    subprocess.run(["python3", "ai_agent.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
