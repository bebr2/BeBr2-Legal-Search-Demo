'''
统计extract_xml得到的各字段的结果
'''


import os
import re
import json

output_path = "../data/processed"

names = os.listdir(output_path)
need_index_key = ["wsmc", "year", "reason", "province", "ajlbsimple", "fywszl-wszl", "wszzdw"]

stat_result = {
    key: set() for key in need_index_key
}

wsmc = set()

if __name__ == "__main__":
    for name in names:
        with open(os.path.join(output_path, name), "r", encoding="utf-8") as f:
            data = json.load(f)
        wsmc.add(data["wsmc"] if data["wsmc"] is not None else (data["fywszl-wszl"] if data["fywszl-wszl"] != "暂予监外执行案例" else None))
        for key in need_index_key:
            if key in ["reason", "ft"]:
                if data[key] is not None:
                    for reason in data[key]:
                        stat_result[key].add(reason)
            else:
                stat_result[key].add(data[key])
                if key == "year" and data[key] == "0051":
                    print(name)
                    exit()

    for key in need_index_key:
        print(key, len(stat_result[key]), stat_result[key])

    print(wsmc)