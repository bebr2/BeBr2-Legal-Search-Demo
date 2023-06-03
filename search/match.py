'''
用于类案匹配的模块
'''

import os
import faiss
import json
import sqlite3
import random

import sys
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "flask"))
from config import *

# 可以选择是否加载Lawformer模型
if USE_LAWFORMER_MATCH:
    from transformers import AutoModel, AutoTokenizer
    tokenizer_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../data/tokenizer")
    model_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../data/lawformer")
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
    model = AutoModel.from_pretrained(model_path)
    model.eval()
    vector_index_path = "../data/vector_index/vector.index"
    vector_index = faiss.read_index(os.path.join(os.path.abspath(os.path.dirname(__file__)), vector_index_path))


with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "../data/order.json"), "r", encoding="utf-8") as f:
    order = json.load(f)
    order = [name.split(".")[0] for name in order]
    
conn = sqlite3.connect(os.path.join(os.path.abspath(os.path.dirname(__file__)), "../data/ft2wsmc.db"),  check_same_thread=False)
cursor = conn.cursor()

# 文本转换为稠密向量，第二个参数是截断
def text2vector(text, max_length=4096):
    assert USE_LAWFORMER_MATCH
    inputs = tokenizer(text, return_tensors="pt", max_length=max_length, truncation=True)
    return model(**inputs).last_hidden_state[0][0].unsqueeze(0).detach()

# 类案匹配的函数，先用稠密向量检索（可选），再用bm25筛选。
def match(text, max_length=500, limit=10, bm25=False, vector_limit=None, bm25_p=0, search_func=None):
    if USE_LAWFORMER_MATCH:
        if isinstance(text, str):
            vector = text2vector(text, max_length).numpy().astype("float32")
            faiss.normalize_L2(vector)
        else:
            # reshape到(1,768)
            vector = text.reshape(1, 768)
    if bm25:
        assert search_func is not None
        assert isinstance(text, str)
        if USE_LAWFORMER_MATCH:
            assert vector_limit is not None
            _, I = vector_index.search(vector, vector_limit)
            result = [order[i] for i in I[0]]
        else:
            result = None
        return search_func({"text": text, "id_": result}, limit=limit, p=bm25_p)
    else:
        assert USE_LAWFORMER_MATCH
        D, I = vector_index.search(vector, limit)
        if bm25_p > 0:
            assert len(I[0]) >= 2
            top2_score = D[0][1]
            I = [[i for t, i in enumerate(I[0]) if D[0][t] >= top2_score * bm25_p]]
        return [order[i] for i in I[0]]

# 从sql数据库中获得该案件法条匹配的类案，随机返回num条
def get_match_ft(ft, num):
    cursor.execute("select wsmc from ft2wsmc where ft = ?", (ft,))
    result = cursor.fetchall()
    return [] if len(result) == 0 else random.sample(result, min(num, len(result)))

# 从sql数据库中获得该案件文本匹配的类案，随机返回num条
def get_match_text(docid, num):
    cursor.execute("select match1, match2, match3, match4, match5, match6, match7, match8 from match where id = ?", (docid,))
    result = cursor.fetchall()
    if len(result) == 0 or len(result[0]) == 0:
        return []
    result = [r for r in result[0] if r != ""]
    return random.sample(result, min(num, len(result)))