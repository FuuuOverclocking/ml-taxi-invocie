import cv2
from util import *


for img, label in img_label_generator():
    cv2.imwrite("./aaa.jpg", img)
    print(label)

    break
