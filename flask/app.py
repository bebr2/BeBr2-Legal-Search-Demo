from flask import Flask, jsonify, request
import sys
import json
import os
import time
import re
import jieba
jieba.initialize()
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "search"))
from trie_tree import get_recommend_words
from config import *
from match import match, get_match_ft, get_match_text
if USE_WHOOSH_SEARCH:
    from search import search
else:
    from es_search import search

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 禁止中文转义

json_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "data", "processed")


# 关键词搜索的函数，从前端获得关键词，及精细化搜索的条件，返回搜索结果
# 结果包含：docid, year, ajlbsimple, title, text的一部分，以及搜索时间
@app.route('/search', methods=['POST'])
def appsearch():
    # 从前端获得关键词
    try:
        data = request.json
        query = data["text"]
        if query is not None and len(query) > 30:
            query = query[:30]
        start = time.time()
        res = search(data, limit=SEARCH_LIMIT)
        end = time.time()
        result = []
        for r in res:
            with open(os.path.join(json_path, f"{r}.json"), encoding="utf-8") as f:
                data = json.load(f)
            result.append({
            "docid": r,
            "year": data["year"] if "year" in data and data["year"] is not None else "未知",
            "ajlbsimple": data["ajlbsimple"] if "ajlbsimple" in data and data["ajlbsimple"] is not None else "未归类",
            "title": data["title"],
            "text": data["text"].replace(data["title"], "").strip()[:200],
            "reason": "、".join(data["reason"]) if "reason" in data and data["reason"] is not None else "未总结"
        })
        return jsonify({'code': 200, 'result': result, 'time': end - start, 'segment': [] if query is None else sorted(list(jieba.cut_for_search(query)), key=lambda x: len(x), reverse=True)})
    except Exception as e:
        print(e)
            
# 类案匹配的函数，从前端获得上传的文件，返回匹配结果
# 结果包含：docid, year, ajlbsimple, title, text的一部分，以及匹配时间
@app.route('/match', methods=['POST'])
def appmatch():
    # 从前端获得上传的文件
    file = request.files.get('file')
    if file is None:
        return jsonify({'code': 401})
    content = file.read().decode('utf-8')
    start = time.time()
    res = match(content, 512, MATCH_LIMIT, bm25=USE_BM25_MATCH, bm25_p=0.8, search_func=search)
    end = time.time()
    result = []
    for r in res:
        with open(os.path.join(json_path, f"{r}.json"), encoding="utf-8") as f:
            data = json.load(f)
        result.append({
            "docid": r,
            "year": data["year"] if "year" in data and data["year"] is not None else "未知",
            "ajlbsimple": data["ajlbsimple"] if "ajlbsimple" in data and data["ajlbsimple"] is not None else "未归类",
            "title": data["title"],
            "text": data["text"].replace(data["title"], "").strip(),
            "reason": "、".join(data["reason"]) if "reason" in data and data["reason"] is not None else "未总结"
        })
    return jsonify({'code': 200, 'result': result, 'time': end - start})

# 文章展示时获取文章内容的函数，从前端获得docid，返回文章内容
# 结果包含：match_content, result
@app.route('/show', methods=['POST'])
def appshow():
    # 从前端获得docid
    docid = request.json.get('docid')
    try:
        with open(os.path.join(json_path, f"{docid}.json"), encoding="utf-8") as f:
            data = json.load(f)
    except:
        return jsonify({'code': 401})
    # 处理None的情况，替换为“未知”““未归类”等，前端就不处理了
    for k in data:
        if data[k] is None and k != "ft" and k != "reason":
            data[k] = "未知"
    if data["reason"] is None or data["reason"] == []:
        data["reason"] = ["未总结"]
    if data["ajlx-ajlb"] != "未知":
        data["ajlbsimple"] = data["ajlx-ajlb"]
    elif data["ajlbsimple"] != "未知":
        if not data["ajlbsimple"].endswith("案件"):
            data["ajlbsimple"] += "案件"
    data["jbjg"] = data["jbfy-cbjg"]
    ft_match = []
    if data["ft"] is None or data["ft"] == []:
        data["ft"] = ["未提取"]
    else:
        for ft in data["ft"]:
            res = get_match_ft(ft, 3)
            res = [r[0] for r in res if r[0] != docid]
            if not res:
                res = [[0, "无匹配"]]
            else:
                for i in range(len(res)):
                    with open(os.path.join(json_path, f"{res[i]}.json"), encoding="utf-8") as f:
                        res[i] = [int(res[i]), json.load(f)["ah"]]
            ft_match.append([ft, res])
    text_match = get_match_text(docid, 3)
    text_match_with_ah = []
    for docid in text_match:
        with open(os.path.join(json_path, f"{docid}.json"), encoding="utf-8") as f:
            text_match_with_ah.append([int(docid), json.load(f)["ah"]])
            
    # 处理正文分段，标点符号+空格的形式，把空格替换为\n
    text = data["text"]
    text = text.replace(data["title"], "").strip()
    text = re.sub(r"([。！？；])\s", r"\1\n", text)
    data["text"] = text.split("\n")
    data["text_wm"] = data["text"].pop().split(" ") if data["text"][-1].startswith("审") else []
    return jsonify({'code': 200, 'match_content': [ft_match, text_match_with_ah], 'result': data})

# 获得查询词的推荐词的函数，从前端获得查询词，返回推荐词，是Get方法
# 结果包含：recommend_words
@app.route('/recommend', methods=['GET'])
def recommend():
    # 从前端获得查询词
    query = request.args.get('query')
    recommend_words = get_recommend_words(query, 8)
    return jsonify({'code': 200, 'suggestions': recommend_words})     

if __name__ == '__main__':
    app.run(host="0.0.0.0")