'''
建立一个sqlite3数据库
ft字段建立索引
另外一个表，存储id到match_legal的映射

注意./flask/config.py下，USE_LAWFORMER_MATCH设置为真，且USE_BM25_MATCH设置为假，才能跑本程序
'''



import os
import json
import sqlite3
import tqdm
import sys
import json
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "search"))
from match import match, vector_index, order

data_path = "../data/processed"

conn = sqlite3.connect("../data/ft2wsmc.db")
c = conn.cursor()

c.execute('''CREATE TABLE ft2wsmc
                (ft text, wsmc text)''')

match_result = {}
for i, name in tqdm.tqdm(enumerate(order)):
    with open(os.path.join(data_path, f"{name}.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    if data["ft"] is not None:
        for ft in data["ft"]:
            c.execute("INSERT INTO ft2wsmc VALUES (?, ?)", (ft, name))
    res = match(vector_index.reconstruct(i), 1024, 9, False, bm25_p = 0.5)
    match_result[name] = [r for r in res if r != name][:8]

c.execute("CREATE INDEX ft_index ON ft2wsmc (ft)")
print(
    f"平均匹配长度：{sum(len(match_result[key]) for key in match_result) / len(match_result)}"
)

# 新建match表，id是主键
c.execute('''CREATE TABLE match
                (id text, match1 text, match2 text, match3 text, match4 text, match5 text, match6 text, match7 text, match8 text)''')
for name in tqdm.tqdm(order):
    match_result[name] += [""] * (8 - len(match_result[name]))
    c.execute("INSERT INTO match VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, *match_result[name]))

conn.commit()
            