import os
import sys
import numpy as np

# コマンドライン引数からファイル名と出力パス（オプション）を取得
if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage: Formatter.py <filename> [<output_path>]")
    sys.exit(1)

filename = sys.argv[1]
output_path = sys.argv[2] if len(sys.argv) == 3 else "./outputs"
output_filename = os.path.join(output_path, f"FomattedPos_{filename}.csv")

# .txtファイルロードリストに格納
data = np.load(filename, allow_pickle=True)
list1 = [] 
for frame in range(len(data)):
    strvalue = ""
    for joints in range(len(data[frame])):
        strvalue += str(data[frame][joints][0])  +", " + str(data[frame][joints][1])  +", " + str(data[frame][joints][2]) + ", "
    list1.append(strvalue[:-2])

with open(output_filename, "w") as f:
    for item in list1:
        f.write(f"{item}\n")