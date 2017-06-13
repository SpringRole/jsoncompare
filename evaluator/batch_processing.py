import csv
import glob
import os

output_dir = os.getcwd() + "/output"
target_dir = os.getcwd() + "/target"

# output files
out_list = []
output_files = glob.glob(output_dir + "/*.json")
for f in output_files:
    out_list.append(f[f.rfind("/") + 1:])

# target files
tar_list = []
target_files = glob.glob(target_dir + "/*.json")
for f in target_files:
    tar_list.append(f[f.rfind("/") + 1:])

# initialising result file
res = [["hits", "miss", "accuracy", "F1 score"]]
with open("result.csv", "w") as result:
    writer = csv.writer(result)
    writer.writerows(res)
result.close()

# running evaluator
for output in out_list:
    if output in tar_list:
        print("\n")
        print(output)
        args = target_dir + "/" + output + " " + output_dir + "/" + output
        os.system("python3 compare.py " + args)
    else:
        print("Target", output, "not found")

# calculating aggregate values
hits = []
miss = []
accuracy = 0
score=[]
with open("result.csv") as result:
    reader = csv.DictReader(result)
    for row in reader:
        hits.append(int(row["hits"]))
        miss.append(int(row["miss"]))
        score.append(float(row["F1 score"]))
    hits = sum(hits)
    miss = sum(miss)
    score=sum(score)/len(score)
    if miss or hits:
        accuracy = hits / (hits + miss) * 100
    print("\nTotal hits :", hits)
    print("Total miss :", miss)
    print("Aggregate accuracy :", accuracy, "%")
    print("Aggregate F1 score :", score)
