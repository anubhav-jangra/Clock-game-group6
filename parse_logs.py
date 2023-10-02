import glob
import argparse
import numpy as np
import collections
import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("--comment", "-com", default = "Test", help="Pass a comment to be saved in the analysis file.")

args = parser.parse_args()
_comment = args.comment

logs_path = "logs/log_moves_*.txt"
analysis_file_path = "analysis.txt"

analysis_file = open(analysis_file_path, 'a')

print(f"\n\n~~~~~~~~~{_comment}~~~~~~~", file=analysis_file)

print("Total runs:", len(glob.glob(logs_path)))

print("Total runs:", len(glob.glob(logs_path)), file=analysis_file)

print([x for x in sorted(glob.glob(logs_path))])

winners = []
time_to_choose_p1 = []
time_to_choose_p2 = []
time_to_choose_p3 = []

time_to_decide_p1 = []
time_to_decide_p2 = []
time_to_decide_p3 = []

scores_p1 = []
scores_p2 = []
scores_p3 = []

all_constraint_sizes_p1 = []
all_constraint_sizes_p2 = []
all_constraint_sizes_p3 = []

satisfied_p1 = []
satisfied_p2 = []
satisfied_p3 = []

count_satisfied_p1 = []
count_satisfied_p2 = []
count_satisfied_p3 = []

unsatisfied_p1 = []
unsatisfied_p2 = []
unsatisfied_p3 = []

count_unsatisfied_p1 = []
count_unsatisfied_p2 = []
count_unsatisfied_p3 = []

print("Analyzing the runs...")
for _file in tqdm.tqdm(sorted(glob.glob(logs_path))):
    content = open(_file).read().split("\n")

    if content[-2] == "Simulation terminated due to excess time taken.":
        winners.append("TLE!")
        continue

    # Find the winner
    if content[-4] == "No winner here it's a tie. Or maybe you both (or all of you) are the winners!!":
        winners.append("Draw")
    else:
        winner = int(content[-4].split("Congratulations Player ")[1].split(" you are the winner!!!")[0])
        winners.append("Player " + str(winner))
    
    # Total time to chooose
    choose_time_p1 = float(content[-3].split("Time taken by player 1, 2 and 3 to choose : [")[1].split("]")[0].split(", ")[0])
    choose_time_p2 = float(content[-3].split("Time taken by player 1, 2 and 3 to choose : [")[1].split("]")[0].split(", ")[1])
    choose_time_p3 = float(content[-3].split("Time taken by player 1, 2 and 3 to choose : [")[1].split("]")[0].split(", ")[2])
    
    time_to_choose_p1.append(choose_time_p1)
    time_to_choose_p2.append(choose_time_p2)
    time_to_choose_p3.append(choose_time_p3)

    # Total time to decide
    decide_time_p1 = float(content[-2].split("Total time taken by player 1, 2 and 3 to decide moves : [")[1].split("]")[0].split(", ")[0])
    decide_time_p2 = float(content[-2].split("Total time taken by player 1, 2 and 3 to decide moves : [")[1].split("]")[0].split(", ")[1])
    decide_time_p3 = float(content[-2].split("Total time taken by player 1, 2 and 3 to decide moves : [")[1].split("]")[0].split(", ")[2])

    time_to_decide_p1.append(decide_time_p1)
    time_to_decide_p2.append(decide_time_p2)
    time_to_decide_p3.append(decide_time_p2)

    # Obtain the individual scores for each run
    score_p1 = int(content[-7].split("Player 1 has score ")[1].split(" with satistied constraints ")[0])
    score_p2 = int(content[-6].split("Player 2 has score ")[1].split(" with satistied constraints ")[0])
    score_p3 = int(content[-5].split("Player 3 has score ")[1].split(" with satistied constraints ")[0])

    scores_p1.append(score_p1)
    scores_p2.append(score_p2)
    scores_p3.append(score_p3)

    # Obtain the data on constraints selected. And what size constraints were satisfied/unsatisfied
    curr_satisfied_p1 = [y for y in [len(x.split('<')) for x in content[-7].split("with satistied constraints [")[1].split("] unsatisfied constraints ")[0].split(', ')] if y != 1]
    curr_satisfied_p2 = [y for y in [len(x.split('<')) for x in content[-6].split("with satistied constraints [")[1].split("] unsatisfied constraints ")[0].split(', ')] if y != 1]
    curr_satisfied_p3 = [y for y in [len(x.split('<')) for x in content[-5].split("with satistied constraints [")[1].split("] unsatisfied constraints ")[0].split(', ')] if y != 1]

    # print(content[-7].split("with satistied constraints [")[1].split("] unsatisfied constraints ")[0].split(', '))
    # print([y for y in [len(x.split('<')) for x in content[-7].split("with satistied constraints [")[1].split("] unsatisfied constraints ")[0].split(', ')] if y != 1])

    satisfied_p1.append(curr_satisfied_p1)
    satisfied_p2.append(curr_satisfied_p2)
    satisfied_p3.append(curr_satisfied_p3)
    
    count_satisfied_p1.append(len(curr_satisfied_p1))
    count_satisfied_p2.append(len(curr_satisfied_p2))
    count_satisfied_p3.append(len(curr_satisfied_p3))

    curr_unsatisfied_p1 = [y for y in [len(x.split('<')) for x in content[-7].split("unsatisfied constraints [")[1].split("]")[0].split(', ')] if y != 1]
    curr_unsatisfied_p2 = [y for y in [len(x.split('<')) for x in content[-6].split("unsatisfied constraints [")[1].split("]")[0].split(', ')] if y != 1]
    curr_unsatisfied_p3 = [y for y in [len(x.split('<')) for x in content[-5].split("unsatisfied constraints [")[1].split("]")[0].split(', ')] if y != 1]

    unsatisfied_p1.append(curr_unsatisfied_p1)
    unsatisfied_p2.append(curr_unsatisfied_p2)
    unsatisfied_p3.append(curr_unsatisfied_p3)

    count_unsatisfied_p1.append(len(curr_unsatisfied_p1))
    count_unsatisfied_p2.append(len(curr_unsatisfied_p2))
    count_unsatisfied_p3.append(len(curr_unsatisfied_p3))


print("Winner stats - \n", collections.Counter(winners), "\n")

print("Choosing time p1 - \n", time_to_choose_p1)
print("Avg - ", np.mean(time_to_choose_p1), "Std Dev - ", np.std(time_to_choose_p1))
print("Choosing time p2 - \n", time_to_choose_p2)
print("Avg - ", np.mean(time_to_choose_p2), "Std Dev - ", np.std(time_to_choose_p2))
print("Choosing time p3 - \n", time_to_choose_p3)
print("Avg - ", np.mean(time_to_choose_p3), "Std Dev - ", np.std(time_to_choose_p3), "\n\n")

print("Decision time p1 - \n", time_to_decide_p1)
print("Avg - ", np.mean(time_to_decide_p1), "Std Dev - ", np.std(time_to_decide_p1))
print("Decision time p2 - \n", time_to_decide_p2)
print("Avg - ", np.mean(time_to_decide_p2), "Std Dev - ", np.std(time_to_decide_p2))
print("Decision time p3 - \n", time_to_decide_p3)
print("Avg - ", np.mean(time_to_decide_p3), "Std Dev - ", np.std(time_to_decide_p3), "\n\n")

print("Scores p1 - \n", scores_p1)
print("Avg - ", np.mean(scores_p1), "Std dev - ", np.std(scores_p1))
print("Scores p2 - \n", scores_p2)
print("Avg - ", np.mean(scores_p2), "Std dev - ", np.std(scores_p2))
print("Scores p3 - \n", scores_p3)
print("Avg - ", np.mean(scores_p3), "Std dev - ", np.std(scores_p3), "\n\n")

print("Satisfied constraints p1 - \n", count_satisfied_p1)
print("Avg - ", np.mean(count_satisfied_p1), "Std dev - ", np.std(count_satisfied_p1))
print("Satisfied constraints p2 - \n", count_satisfied_p2)
print("Avg - ", np.mean(count_satisfied_p2), "Std dev - ", np.std(count_satisfied_p2))
print("Satisfied constraints p3 - \n", count_satisfied_p3)
print("Avg - ", np.mean(count_satisfied_p3), "Std dev - ", np.std(count_satisfied_p3), "\n\n")

print("Count Satisfied constraints p1 - \n", satisfied_p1)
print("Count Satisfied constraints p2 - \n", satisfied_p2)
print("Count Satisfied constraints p3 - \n", satisfied_p3, "\n\n")

print("Unatisfied constraints p1 - \n", count_unsatisfied_p1)
print("Avg - ", np.mean(count_unsatisfied_p1), "Std dev - ", np.std(count_unsatisfied_p1))
print("Unatisfied constraints p2 - \n", count_unsatisfied_p2)
print("Avg - ", np.mean(count_unsatisfied_p2), "Std dev - ", np.std(count_unsatisfied_p2))
print("Unsatisfied constraints p3 - \n", count_unsatisfied_p3)
print("Avg - ", np.mean(count_unsatisfied_p3), "Std dev - ", np.std(count_unsatisfied_p3), "\n\n")

print("Count Unsatisfied constraints p1 - \n", unsatisfied_p1)
print("Count Unsatisfied constraints p2 - \n", unsatisfied_p2)
print("Count Unsatisfied constraints p3 - \n", unsatisfied_p3, "\n\n")

# Write down the same thing to the analysis file

print("Winner stats - \n", str(collections.Counter(winners)), "\n", file=analysis_file)

print("Choosing time p1 - \n", time_to_choose_p1, file=analysis_file)
print("Avg - ", np.mean(time_to_choose_p1), "Std Dev - ", np.std(time_to_choose_p1), file=analysis_file)
print("Choosing time p2 - \n", time_to_choose_p2, file=analysis_file)
print("Avg - ", np.mean(time_to_choose_p2), "Std Dev - ", np.std(time_to_choose_p2), file=analysis_file)
print("Choosing time p3 - \n", time_to_choose_p3, file=analysis_file)
print("Avg - ", np.mean(time_to_choose_p3), "Std Dev - ", np.std(time_to_choose_p3), "\n\n", file=analysis_file)

print("Decision time p1 - \n", time_to_decide_p1, file=analysis_file)
print("Avg - ", np.mean(time_to_decide_p1), "Std Dev - ", np.std(time_to_decide_p1), file=analysis_file)
print("Decision time p2 - \n", time_to_decide_p2, file=analysis_file)
print("Avg - ", np.mean(time_to_decide_p2), "Std Dev - ", np.std(time_to_decide_p2), file=analysis_file)
print("Decision time p3 - \n", time_to_decide_p3, file=analysis_file)
print("Avg - ", np.mean(time_to_decide_p3), "Std Dev - ", np.std(time_to_decide_p3), "\n\n", file=analysis_file)

print("Scores p1 - \n", scores_p1, file=analysis_file)
print("Avg - ", np.mean(scores_p1), "Std dev - ", np.std(scores_p1), file=analysis_file)
print("Scores p2 - \n", scores_p2, file=analysis_file)
print("Avg - ", np.mean(scores_p2), "Std dev - ", np.std(scores_p2), file=analysis_file)
print("Scores p3 - \n", scores_p3, file=analysis_file)
print("Avg - ", np.mean(scores_p3), "Std dev - ", np.std(scores_p3), "\n\n", file=analysis_file)

print("Satisfied constraints p1 - \n", count_satisfied_p1, file=analysis_file)
print("Avg - ", np.mean(count_satisfied_p1), "Std dev - ", np.std(count_satisfied_p1), file=analysis_file)
print("Satisfied constraints p2 - \n", count_satisfied_p2, file=analysis_file)
print("Avg - ", np.mean(count_satisfied_p2), "Std dev - ", np.std(count_satisfied_p2), file=analysis_file)
print("Satisfied constraints p3 - \n", count_satisfied_p3, file=analysis_file)
print("Avg - ", np.mean(count_satisfied_p3), "Std dev - ", np.std(count_satisfied_p3), "\n\n", file=analysis_file)

print("Count Satisfied constraints p1 - \n", satisfied_p1, file=analysis_file)
print("Count Satisfied constraints p2 - \n", satisfied_p2, file=analysis_file)
print("Count Satisfied constraints p3 - \n", satisfied_p3, "\n\n", file=analysis_file)

print("Unatisfied constraints p1 - \n", count_unsatisfied_p1, file=analysis_file)
print("Avg - ", np.mean(count_unsatisfied_p1), "Std dev - ", np.std(count_unsatisfied_p1), file=analysis_file)
print("Unatisfied constraints p2 - \n", count_unsatisfied_p2, file=analysis_file)
print("Avg - ", np.mean(count_unsatisfied_p2), "Std dev - ", np.std(count_unsatisfied_p2), file=analysis_file)
print("Unsatisfied constraints p3 - \n", count_unsatisfied_p3, file=analysis_file)
print("Avg - ", np.mean(count_unsatisfied_p3), "Std dev - ", np.std(count_unsatisfied_p3), "\n\n", file=analysis_file)

print("Count Unsatisfied constraints p1 - \n", unsatisfied_p1, file=analysis_file)
print("Count Unsatisfied constraints p2 - \n", unsatisfied_p2, file=analysis_file)
print("Count Unsatisfied constraints p3 - \n", unsatisfied_p3, "\n\n", file=analysis_file)
