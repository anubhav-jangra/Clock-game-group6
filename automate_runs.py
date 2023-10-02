import os
import sys
import tqdm
import shutil
import subprocess

# remove the logs file before starting a new run
if os.path.exists("logs"):
    shutil.rmtree("logs")

# Edit this comment for the changes you do on the simulation
comment = "P6/P7/P8 First run of greedy search. 10 runs. Seed 1 to 10"

# Todo - need to add a flag for #constraints.

# The fonal results will be saved in analysis.txt

run_size = 10
player_0 = 6
player_1 = 7
player_2 = 8
for idx, seed_val in tqdm.tqdm(enumerate(range(run_size)), total=run_size, file=sys.stdout):
    subprocess.run(["python", "clock_game_auto.py", "--no_gui", "True", "--seed" , str(seed_val), "--p0", str(player_0), "--p1", str(player_1), "--p2", str(player_2), "--run_id", str(idx)])

subprocess.run(["python", "parse_logs.py", "--comment", comment])
