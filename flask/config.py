# 用whoosh或es搜索
USE_WHOOSH_SEARCH = True

# 搜索返回个数
SEARCH_LIMIT = 40

# 匹配返回个数
MATCH_LIMIT = 40

# 案件匹配是否用lawformer
USE_LAWFORMER_MATCH = False

# 案件匹配是否用bm25
USE_BM25_MATCH = True

assert USE_LAWFORMER_MATCH or USE_BM25_MATCH