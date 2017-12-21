import json
import sys
from itertools import repeat
from sklearn.metrics import f1_score
import jsoncompare


def compare(a, b):
    miss, hit, actual = jsoncompare.json_are_same(a, b)[1:4]
    expected = []
    expected.extend(repeat(1, len(actual)))
    hit_val = hit[1]
    miss_val = miss[1]
    accuracy = hit_val / (hit_val + miss_val) * 100

    score = f1_score(expected, actual)
    print("**********")
    print("hits =", hit_val)
    print("miss =", miss_val)
    print("accuracy =", accuracy, "%")
    print("f1 score =", score)

    # writing results of each file in a csv file
    # res = [[hit_val, miss_val, accuracy, score]]
    # with open("result.csv", "a"   ) as result:
    #     writer = csv.writer(result)
    #     writer.writerows(res)


if __name__ == "__main__":
    file1 = sys.argv[1]  # target json
    file2 = sys.argv[2]  # output json
    with open(file1) as f:
        a = json.dumps(json.load(f), sort_keys=True)
    with open(file2) as f:
        b = json.dumps(json.load(f), sort_keys=True)
    compare(a, b)
