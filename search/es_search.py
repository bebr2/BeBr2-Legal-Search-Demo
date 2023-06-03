'''
用elastic search重新实现的搜索算法，比whoosh快很多
'''

from elasticsearch import Elasticsearch

es = Elasticsearch(hosts="http://localhost:9200")

filter_fields = ["wszzdw", "wsmc", "province", "ajlbsimple"]

# 搜索的函数，传入各个字段的搜索词，返回搜索结果
# year是一个tuple(起始年份，终止年份)
# p未实现，暂时不用
def search(search_dict, limit=10, p=0):
    query = {
            "query": {
                "bool": {
                    
                }
            },
            "size": limit,
            "sort": [
                {
                    "_score": {"order": "desc"}   # 按相关度得分降序排列
                }
            ]
        }
    for f in filter_fields:
        if f in search_dict and search_dict[f] is not None:
            if "must" not in query["query"]["bool"]:
                query["query"]["bool"]["must"] = []
            query["query"]["bool"]["must"].append({"match": {f: {"query": search_dict[f], "analyzer": "keyword"}}})
    if "id_" in search_dict and search_dict["id_"] is not None:
        if "must" not in query["query"]["bool"]:
            query["query"]["bool"]["must"] = [{"terms": search_dict["id_"]}]
        else:
            query["query"]["bool"]["must"].append({"terms": search_dict["id_"]})
    if "text" in search_dict and search_dict["text"] is not None:
        if "should" not in query["query"]["bool"]:
            query["query"]["bool"]["should"] = []
        query["query"]["bool"]["should"].append({"match":{"text":{"query": search_dict["text"], "analyzer": "ik_smart"}}})
    if "reason" in search_dict and search_dict["reason"] is not None:
        if "should" not in query["query"]["bool"]:
            query["query"]["bool"]["should"] = []
        query["query"]["bool"]["should"].append({"match":{"reason":{"query": search_dict["reason"], "analyzer": "ik_smart"}}})
    if "year" in search_dict and search_dict["year"] is not None:
        if "must" not in query["query"]["bool"]:
            query["query"]["bool"]["must"] = [{"range": {}}]
        else:
            query["query"]["bool"]["must"].append({"range": {}})
        query["query"]["bool"]["must"][-1]["range"]["year"] = {"gte": search_dict["year"][0], "lte": search_dict["year"][1]}
    
    result = es.search(index="legal_index", body=query)

    return [hit["_source"]["id"] for hit in result["hits"]["hits"]]

