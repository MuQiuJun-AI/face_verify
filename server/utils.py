import base64
import numpy as np
import cv2
import requests
import json


def image_to_base64(img):
    """
    对ndarray数组进行base64编码， 保证图片的channal顺序保持不变， 即不会把rgb编码成bgr，或者把bgr编码成rgb
    :param img:
    :return:
    """
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    retval, buffer = cv2.imencode('.jpg', img)
    pic_str = base64.b64encode(buffer)
    pic_str = pic_str.decode()
    return pic_str


def base64_to_image(base64_str):
    """
    把base64字符串转化成ndarray， 保证图片的channal顺序保持不变， 即不会把rgb解码成bgr，或者把bgr解码成rgb
    :param img:
    :return:
    """
    data = base64.b64decode(base64_str)
    img_data = np.fromstring(data, np.uint8)
    image = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


def http_post(url, data_dic):
    r = requests.post(url=url, data=json.dumps(data_dic))
    return r.json()
