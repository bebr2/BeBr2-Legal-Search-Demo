'''
建立稠密向量索引
'''
import faiss
import numpy as np
import os
import tqdm
import sys
import json
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "search"))
from search import text2vector

data_path = "../data/processed"
index_path = "../data/vector_index/vector.index"

dim = 768

if __name__ == "__main__":
    index = faiss.IndexFlatIP(dim)
    names = os.listdir(data_path)
    for name in tqdm.tqdm(names):
        with open(os.path.join(data_path, name), "r", encoding="utf-8") as f:
            data = json.load(f)
        features = text2vector(data["text"], 1024).numpy().astype('float32')
        faiss.normalize_L2(features)
        index.add(features)
    faiss.write_index(index, index_path)
    with open("../data/order.json", "w+", encoding="utf-8") as f:
        json.dump(names, f, ensure_ascii=False, indent=4)