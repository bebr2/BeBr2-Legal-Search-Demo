'''
用whoosh库建立索引
需要建立索引的字段：
text、wszzdw、wsmc、year、reason、province、ajlbsimple、fywszl-wszl
其中year是INT，其他都是TEXT
text和reason是检索字段，其他都是筛选字段
构建索引前去除停用词
'''

import os
import json
import tqdm

data_path = "../data/processed"
index_path = "../data/index"

from whoosh.index import create_in
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer
from utils import stop_list

if __name__ == "__main__":
    analyzer = ChineseAnalyzer(stoplist=stop_list)
    schema = Schema(
        id_ = ID(stored=True),
        text=TEXT(stored=True, analyzer=analyzer),
        wszzdw=TEXT(stored=True),
        wsmc=TEXT(stored=True),
        year=NUMERIC(stored=True),
        reason=TEXT(stored=True, analyzer=analyzer),
        province=TEXT(stored=True),
        ajlbsimple=TEXT(stored=True),
    )

    ix = create_in(index_path, schema)

    writer = ix.writer()

    names = os.listdir(data_path)

    for name in tqdm.tqdm(names):
        with open(os.path.join(data_path, name), "r", encoding="utf-8") as f:
            data = json.load(f)
        writer.add_document(
            id_=name.split(".")[0],
            text=data["text"],
            wszzdw=data["wszzdw"],
            wsmc=data["wsmc"] if data["wsmc"] is not None else (data["fywszl-wszl"] if data["fywszl-wszl"] != "暂予监外执行案例" else None),
            year=int(data["year"]) if data["year"] is not None else None,
            reason=" ".join(data["reason"]) if data["reason"] is not None else None,
            province=data["province"],
            ajlbsimple=data["ajlbsimple"],
        )

    writer.commit()


    
    
    