from util import *
import cv2


def fill_0(num):
    if num < 10:
        return '00' + str(num)
    if num < 100:
        return '0' + str(num)
    return str(num)


all = read_json('./data/train-label.json')

for img_info in all:
    path = img_info["path"].encode('gbk')
    path = path.decode('gbk')

    img = cv2.imread(path)
    img_id = img_info["id"]
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
        filename = f"{fill_0(img_id)}-{i}.jpg"
        cv2.imwrite(f"./data/train-cropped/{filename}", cropped)
