import requests
from bs4 import BeautifulSoup
import os
import sys
from datetime import datetime
import time
import random
import difflib

# コマンドライン引数からファイル名と出力パス（オプション）を取得
if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage: getlink_mcmod.py <filename> [<output_path>]")
    sys.exit(1)

# コマンドライン引数からファイル名と出力パス（オプション）を取得
ifname = sys.argv[1]
output_path = sys.argv[2] if len(sys.argv) == 3 else os.getcwd()
ofname = os.path.join(output_path, f"output_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")

# 指定文字列を含む行を無視するリスト
ignore_list = ["基本：", "辅助类：", "前置："]

# リンク抽出時に指定文字列が含まれているかチェックする文字列
linkcheckstr = "https://www.mcmod.cn/class/"

# ファイルを読み込み、指定文字列を含む行を無視する
with open(ifname, "r", encoding="utf-8") as f:
    lines = f.readlines()
    result = []
    for line in lines:
        line = line.strip()
        if line and not any(ignore in line for ignore in ignore_list):  # 忽略空白行和包含指定文字列的行
            result.append(line)

# リンクを取得
urls = []
for item in result:
    # mcmod.cnの検索で"复杂搜索"オプションを指定して検索するurlを生成
    url = "https://search.mcmod.cn/s?key="+str(item).lstrip('[\'').rstrip('\']')+"&site=&filter=0&mold=1"
    
    # リクエスト間の遅延をランダムに設定, サーバへの負荷を軽減するため
    delay = random.uniform(1, 5)
    time.sleep(delay)

    # リクエストを送信し、レスポンスを取得
    r = requests.get(url)
    html = r.content
    # BeautifulSoupで解析
    soup = BeautifulSoup(html, 'html.parser')
    # すべてのaタグを取得
    a_tag = soup.find_all('a')
    
    #類似度の初期化
    target = [0,0]

    for i in range(len(a_tag)):
        # 検索文字列と検索結果との類似度が最も高いリンクを取得  
        s = difflib.SequenceMatcher(None, item, a_tag[i].text)
        similarity = s.ratio()
        if similarity > target[0]:
            if linkcheckstr not in a_tag[i]['href']:
                continue
            target[0] = similarity
            target[1] = i
    # 類似度が0.4以上の場合、リンクを取得
    if target[0] > 0.4:   
        print(a_tag[target[1]]['href'])
        urls.append(a_tag[target[1]]['href'])
    else:
        urls.append('未找到目标链接')
        print('未找到目标链接')

# リンクをファイルに書き込み
with open(ofname, "w", encoding='utf-8') as f:
    for i in range(len(urls)):
        f.write(f"[{result[i]}]({urls[i]})\n")
