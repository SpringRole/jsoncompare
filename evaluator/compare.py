import json

from jsoncompare import jsoncompare

file1 = "file1.json"  # target json
file2 = "file2.json"  # parsed json

with open(file1) as f:
    a = json.load(f)

with open(file2) as f:
    b = json.load(f)

miss,hit=jsoncompare.are_same(a, b)[1:3]
hit_val=hit[1]
miss_val=miss[1]
print("**********")
print("hits = ",hit_val)
print("miss = ",miss_val)
print("accuracy = ",hit_val/(hit_val+miss_val)*100,"%")
