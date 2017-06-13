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

for output in out_list:
    if output in tar_list:
        print("\n")
        print(output)
        args=target_dir+"/"+output+" "+output_dir+"/"+output
        os.system("python3 compare.py "+args)
    else:
        print("Target", output, "not found")