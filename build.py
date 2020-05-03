import json
import os
import re
from os.path import *

"""
根据文件夹生成目录
"""


def get_tree(filepath):
    # 返回树和树的位置权重
    if isdir(filepath):
        children = [get_tree(join(filepath, i)) for i in os.listdir(filepath)]
        children = sorted(children, key=lambda x: x[1])
        return {'children': [i[0] for i in children], 'label': basename(filepath)}, children[0][1]
    else:
        k = [0x9999, ]
        nums = re.findall('\d+', basename(filepath))
        if nums:
            k = [int(i) for i in nums]
        label = basename(filepath)
        if label.endswith(".txt"):
            label = label[:-4]
            label = re.sub("第\d+(-\d+)?部～", "", label)
        return {'url': filepath, 'label': label}, k


root = "乾隆大藏经"
tree, _ = get_tree(root)
json.dump(tree['children'], open("index.json", 'w'), ensure_ascii=0, indent=2)
