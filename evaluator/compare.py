import json
import sys
from itertools import repeat
from sklearn.metrics import f1_score
from jsoncompare import jsoncompare

def compare(a,b):
    miss, hit, actual = jsoncompare.are_same(a, b)[1:4]
    expected = []
    expected.extend(repeat(1, len(actual)))
    hit_val = hit[1]
    miss_val = miss[1]
    print("**********")
    print("hits =", hit_val)
    print("miss =", miss_val)
    print("accuracy =", hit_val / (hit_val + miss_val) * 100, "%")
    print("f1 score =", f1_score(expected, actual))

if __name__=="__main__":

    file1 = sys.argv[1]  # target json
    file2 = sys.argv[2]  # output json
    with open(file1) as f:
        a = json.load(f)
    with open(file2) as f:
        b = json.load(f)
    compare(a,b)

