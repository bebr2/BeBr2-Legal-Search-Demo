'''
使用es库建立索引
其他说明见get_index.py
'''

import os
import json
import tqdm

data_path = "../data/processed"

from elasticsearch import Elasticsearch
es = Elasticsearch(hosts="http://localhost:9200")

mapping = {
    "properties": {
        "id": {
            "type": "text",
            "analyzer": "keyword"
        },
        "text": {
            "type": "text",
            "analyzer": "ik_max_word"
        },
        "reason": {
            "type": "text",
            "analyzer": "ik_max_word"
        },
        "wszzdw": {
            "type": "text",
            "analyzer": "keyword"
        },
        "wsmc": {
            "type": "text",
            "analyzer": "keyword"
        },
        "province": {
            "type": "text",
            "analyzer": "keyword"
        },
        "ajlbsimple": {
            "type": "text",
            "analyzer": "keyword"
        },
        "year": {
            "type": "integer"
        }
    }
}

# 创建索引
if not es.indices.exists(index="legal_index"):
    es.indices.create(index="legal_index", body={"mappings": mapping})

# 添加文档

if __name__ == "__main__":
    names = os.listdir(data_path)
    for name in tqdm.tqdm(names):
        with open(os.path.join(data_path, name), "r", encoding="utf-8") as f:
            data = json.load(f)
        doc = {
            "id": name.split(".")[0],
            "text": data["text"],
            "wszzdw": data["wszzdw"],
            "wsmc": data["wsmc"] if data["wsmc"] is not None else (data["fywszl-wszl"] if data["fywszl-wszl"] != "暂予监外执行案例" else None),
            "year": int(data["year"]) if data["year"] is not None else None,
            "reason": " ".join(data["reason"]) if data["reason"] is not None else None,
            "province": data["province"],
            "ajlbsimple": data["ajlbsimple"],
        }
        es.index(index='legal_index', document=doc)
