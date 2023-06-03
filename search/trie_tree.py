'''
构建trie树，用于查询补全
'''
import os
import json
import tqdm
words_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../data/lawwords.json")

with open(words_path, "r", encoding="utf-8") as f:
    lawwords_dict = json.load(f)
    
# 长度大于25的词语，以及包含数字的词语去掉
lawwords_dict = {k: v for k, v in lawwords_dict.items() if len(k) <= 25 and not any(char.isdigit() for char in k)}

class TrieNode(object):
    def __init__(self):
        self.children = {}
        self.is_word = False
        self.word = None
        self.hot = 0
        
    def insert(self, word):
        node = self
        for char in word:
            child = node.children.get(char)
            if child is None:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True
        node.word = word
        
    def search(self, word):
        node = self
        for char in word:
            node = node.children.get(char)
            if node is None:
                return None
        return node
    
    def starts_with(self, prefix):
        node = self
        for char in prefix:
            node = node.children.get(char)
            if node is None:
                return []
        return self.get_all_words(node)
    
    def get_all_words(self, node):
        words = []
        if node.is_word:
            words.append(node.word)
        for key, child in node.children.items():
            words.extend(self.get_all_words(child))
        return self.sort_by_important(words)
    
    def sort_by_important(self, words_list):
        return sorted(words_list, key=lambda x: lawwords_dict[x], reverse=True)
    
    
class Trie(object):
    def __init__(self):
        self.root = TrieNode()
        
    def insert(self, word):
        self.root.insert(word)
        
    def search(self, word):
        return self.root.search(word)
    
    def starts_with(self, prefix):
        return self.root.starts_with(prefix)
    
    def get_all_words(self):
        return self.root.get_all_words(self.root)

import time
start = time.time()
trie = Trie()
for word in tqdm.tqdm(lawwords_dict):
    trie.insert(word)
print(f"Trie tree constructed. {time.time() - start}s")

# 从trie树中获得该词语的推荐词语
def get_recommend_words(word, num):
    words = word.split(" ")[-1]
    prefix = " ".join(word.split(" ")[:-1]) + " "
    return [prefix + k for k in trie.starts_with(words)[:num]]
    
# if __name__ == "__main__":
#     start = time.time()
#     print(trie.starts_with("刑事"))
#     print(time.time() - start)
    