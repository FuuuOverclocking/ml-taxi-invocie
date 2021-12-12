# 工具函数

import cv2
import codecs
from pathlib import Path
import csv
import json


def resolve_path(*paths):
    return str(Path(*paths).resolve())


def clamp(input, min, max):
    return min if input < min else max if input > max else input


def is_number(var):
    return type(var) == int or type(var) == float


def read_csv(*paths):
    path = resolve_path(*paths)
    row_list = None
    fieldnames = None

    with open(path, newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        fieldnames = reader.fieldnames
        row_list = [row for row in reader]

    return fieldnames, row_list


def read_json(*paths, encoding="utf-8"):
    with codecs.open(resolve_path(*paths), "r", encoding=encoding) as file:
        return json.load(file)


def write_json(obj, *paths, indent=None, encoding="utf-8"):
    with codecs.open(resolve_path(*paths), "w", encoding=encoding) as file:
        json.dump(obj, file, ensure_ascii=False, indent=indent)


def img_label_generator():
    all = read_json('./data/train-label.json')

    for img_info in all:
        img = cv2.imread(img_info["path"])
        img_width = img_info["width"]
        img_height = img_info["height"]

        for i, box in enumerate(img_info["boxes"]):
            x0 = box['x0']
            y0 = box['y0']
            x1 = box['x1']
            y1 = box['y1']
            x0, y0, x1, y1 = [round(a) for a in [x0, y0, x1, y1]]
            x0 = clamp(x0, 0, img_width - 1)
            x1 = clamp(x1, 0, img_width - 1)
            y0 = clamp(y0, 0, img_height - 1)
            y1 = clamp(y1, 0, img_height - 1)

            cropped = img[y0:y1, x0:x1]
            yield cropped, box["str"]
