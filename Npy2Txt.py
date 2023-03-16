import os
import sys
import numpy as np
from datetime import datetime

# 表示桁数を指定（デフォルトは8桁）
np.set_printoptions(threshold=1e6)

# コマンドライン引数からファイル名と出力パス（オプション）を取得
if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage: Npz2Txt.py <filename> [<output_path>]")
    sys.exit(1)

# ファイル名と出力パスを取得
filename = sys.argv[1]
output_path = sys.argv[2] if len(sys.argv) == 3 else os.getcwd()

# .npzファイルをallow_pickle=Trueでロード
data = np.load(filename, allow_pickle=True)

# ファイル名を取得
FName = filename.split('/')

# 配列をテキストファイルに書き込み、現在のタイムスタンプをファイル名に追加
output_filename = os.path.join(output_path, FName[-1] + f"_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")
with open(output_filename, "w") as f:
    for key in data.files:
        f.write(f"{key}: {data[key]}\n")
