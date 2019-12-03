from server import utils
import time
import cv2
# a = utils.image_to_base64(cv2.resize(cv2.imread('zh2.jpg')[:, :, ::-1], (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC))
# b = utils.image_to_base64(cv2.resize(cv2.imread("ty.jpg")[:, :, ::-1], (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC))
# start = time.time()
# c = utils.http_post("http://localhost:8065/face_verify/api", data_dic={"pic1_base64": a, "pic2_base64": b})
# print(c)
# print(time.time()-start)

import requests

a = requests.post("http://10.194.186.155:9570/ics-python-nlp-v2/api/v2/get_candidate_answers", data={"sent": "你好", "thresh": 0.6})
