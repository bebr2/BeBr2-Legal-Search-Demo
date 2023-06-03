'''
提供bm25搜索算法以及稠密检索算法的接口
'''
# coding:utf-8
import sys
import os

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "process"))

from whoosh.index import open_dir, FileIndex
from whoosh.filedb.filestore import copy_to_ram
from whoosh.qparser import QueryParser, OrGroup
from whoosh.query import Term, Or, And, NumericRange
import whoosh.scoring as wsc

def my_open_dir(dirname):
    index = open_dir(dirname)
    rs = copy_to_ram(index.storage)
    return FileIndex(rs)


index_path = "../data/index"
legal_index = my_open_dir(os.path.join(os.path.abspath(os.path.dirname(__file__)), index_path))

bm25f = wsc.BM25F(B=0.75, content_B=1.0, K1=1.5)
# 用于筛选的字段
filter_fields = ["wszzdw", "wsmc", "province", "ajlbsimple"]

text_parser = QueryParser("text", legal_index.schema, group=OrGroup)
reason_parser = QueryParser("reason", legal_index.schema, group=OrGroup)

# 搜索的函数，传入各个字段的搜索词，返回搜索结果
# year是一个tuple(起始年份，终止年份)
# p是指分数小于top2_score * p的结果不返回
def search(search_dict, limit=None, p=0):
    term_list = [
        Term(field, search_dict[field])
        for field in filter_fields
        if field in search_dict and search_dict[field] is not None
    ]
    text_list = [And(term_list)] if term_list else []
    if "id_" in search_dict and search_dict["id_"] is not None:
        id_list = [Term("id_", id_) for id_ in search_dict["id_"]]
        text_list.append(Or(id_list))
    if "text" in search_dict and search_dict["text"] is not None:
        text_list.append(text_parser.parse(search_dict["text"]))
    if "reason" in search_dict and search_dict["reason"] is not None:
        text_list.append(reason_parser.parse(search_dict["reason"]))
    if "year" in search_dict and search_dict["year"] is not None:
        text_list.append(NumericRange("year", search_dict["year"][0], search_dict["year"][1]))
    
    and_query = And(text_list)
    with legal_index.searcher(weighting=bm25f) as searcher:
        results = searcher.search(and_query, limit=limit)
        if p > 0:
            assert len(results) >= 2
            top2_score = results[1].score
            results = [r for r in results if r.score >= top2_score * p]
        return [r["id_"] for r in results]




    