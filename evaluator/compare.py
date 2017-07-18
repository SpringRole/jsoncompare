"""
This script is used to compare 2 jsons
It compares file1(target) with file2(output) and writes output in result.csv
"""
import csv
import json
import sys
from itertools import repeat
from sklearn.metrics import f1_score
from jsoncompare import jsoncompare


def compare(a, b):
    """ this function uses jsoncompare library to compare 2 files"""
    miss, hit, actual = jsoncompare.are_same(a, b)[1:4]
    # expected value to calculate f1 score
    expected = []
    expected.extend(repeat(1, len(actual)))
    hit_val = hit[1]
    miss_val = miss[1]
    # calculating accuracy
    accuracy = hit_val / (hit_val + miss_val) * 100
    # calculating f1score
    score = f1_score(expected, actual)
    print("**********")
    print("hits =", hit_val)
    print("miss =", miss_val)
    print("accuracy =", accuracy, "%")
    print("f1 score =", score)

    # appending result to a csv file
    res = [[hit_val, miss_val, accuracy, score]]
    with open("result.csv", "a") as result:
        writer = csv.writer(result)
        writer.writerows(res)


if __name__ == "__main__":
    # target json
    file1 = sys.argv[1]
    # output json
    file2 = sys.argv[2]
    with open(file1) as f:
        a = json.load(f)
    with open(file2) as f:
        b = json.load(f)
    compare(a, b)
