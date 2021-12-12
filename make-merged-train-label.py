from util import *
import os
import shutil


def main():
    result = []

    for root, dir_list, file_list in os.walk('./data/raw-train'):
        for filename in file_list:
            if filename[-5:] != '.json':
                continue

            json_path = os.path.join(root, filename)
            item = convert_single_json(json_path)
            if item != None:
                old_path, img_info = item
                shutil.copyfile(old_path, img_info['path'])
                result.append(img_info)

    write_json(result, './data/train-label.json', encoding="utf-8", indent=4)


def fill_0(num):
    if num < 10:
        return '00' + str(num)
    if num < 100:
        return '0' + str(num)
    return str(num)


id_counter = 0


def convert_single_json(json_path: str):
    global id_counter
    json_object = read_json(json_path, encoding="gb2312")

    # 图片 id
    id = id_counter
    id_counter += 1

    # 图片路径, 长宽
    old_path = json_object["imagePath"]
    old_path = "./data/raw-train/" + old_path
    new_path = "./data/train/" + fill_0(id) + '.jpg'

    w = json_object["imageWidth"]
    h = json_object["imageHeight"]

    # 图内框的数量
    number_of_boxes = len(json_object["shapes"])

    if type(old_path) != str:
        raise Exception(f"{old_path}: 路径有问题")

    if not os.path.exists(old_path):
        print(f"{old_path}: 图片不存在")
        return None

    if type(w) != int or type(h) != int or type(number_of_boxes) != int:
        raise Exception(f"{old_path}: w, h, number_of_boxes 有问题")

    boxes = []
    for shape in json_object["shapes"]:
        if shape["shape_type"] != "rectangle":
            print(
                f"{old_path}: 遇到非方框: { shape['shape_type'] }, 点的数量: {len(shape['points'])}")
            continue

        if (len(shape["points"]) != 2):
            print(f'{old_path}: shape 有问题: {shape["points"]}')
            continue

        box = {}
        box["str"] = shape["label"]
        box["x0"], box["y0"] = shape["points"][0]
        box["x1"], box["y1"] = shape["points"][1]

        if (
            type(box["str"]) != str or
            not is_number(box["x0"]) or
            not is_number(box["y0"]) or
            not is_number(box["x1"]) or
            not is_number(box["y1"])
        ):
            print(old_path)
            print(box)
            raise Exception("box 有问题")

        boxes.append(box)

    return old_path, {
        "id": id,
        "path": new_path,
        "width": w,
        "height": h,
        "number_of_boxes": number_of_boxes,
        "boxes": boxes
    }


main()
