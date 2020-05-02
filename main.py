import os
import re
from os.path import *

from flask import Flask, jsonify, send_file, request

root = "乾隆大藏经"
app = Flask(__name__, static_folder=".", static_url_path="/")


def get_tree(filepath):
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
        return {'url': relpath(filepath, root), 'label': label}, k


@app.route("/api/tree")
def tree():
    tree, _ = get_tree(root)
    return jsonify(tree['children'])


@app.route("/api/get_file")
def get_file():
    filepath = request.args['filepath']
    return open(join(root, filepath)).read()


if __name__ == '__main__':
    app.run(port=5555, debug=True)
