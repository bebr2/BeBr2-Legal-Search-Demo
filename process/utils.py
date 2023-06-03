import os

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "../data/stopwords.txt"), "r", encoding="utf-8") as f:
    stop_list = f.readlines()
    stop_list = [word.strip() for word in stop_list]