'''
处理法律词汇，以用于构建字典树，用于查询推荐
'''
import tqdm
import os
import xml.etree.ElementTree as ET
import re
import json

lawwords_dict = {}
with open("../data/thu_lawwords.txt", encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        words = line.strip().split("\t")
        try:
            lawwords_dict[words[0]] = int(words[1])
        except:
            lawwords_dict[words[0]] = 1
        
# 递归遍历节点
def traverse_node(node):
    if "value" in node.attrib:
        # 按中文标点和空格分割
        words = re.split(r"[，。、；：‘’“”（）【】《》\s]", node.attrib["value"])
        if len(words) <= 3:
            new_words = []
            for word in words:
                # 如果不包含中文，跳过
                if not re.search(r"[\u4e00-\u9fa5]", word):
                    continue
                new_words.append(word)
                if word in lawwords_dict:
                    lawwords_dict[word] += 1
                else:
                    lawwords_dict[word] = 1
            if len(new_words) > 1:
                ngram_word = " ".join(new_words)
                if ngram_word  in lawwords_dict:
                    lawwords_dict[ngram_word] += 1
                else:
                    lawwords_dict[ngram_word] = 1
    for child in node:
        traverse_node(child)


data_path = "../data/Legal_data"

if __name__ == "__main__":
    names = os.listdir(data_path)
    for name in tqdm.tqdm(names):
        try:
            # 对于xml文件中有value值的节点，提取出value值，按标点符号和空格分割
            tree = ET.parse(os.path.join(data_path, name))
            root = tree.getroot()
            traverse_node(root)
        except:
            pass
    with open("../data/lawwords.json", "w+", encoding="utf-8") as f:
        json.dump(lawwords_dict, f, ensure_ascii=False)
    print(len(lawwords_dict))
    

    