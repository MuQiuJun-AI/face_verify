from . import utils
import dlib
import logging
import numpy as np
from pkg_resources import resource_filename


detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(resource_filename(__name__, "model/shape_predictor_5_face_landmarks.dat"))
facerec = dlib.face_recognition_model_v1(resource_filename(__name__, "model/dlib_face_recognition_resnet_model_v1.dat"))


def face_encodeing(img):
    dets, scores, idx = detector.run(img, 1, 0)
    if len(dets) != 1:
        logging.info("没有检测到人脸,或者检测到多个人脸")
        return -1, None
    try:
        shape = sp(img, dets[0])
        face_chip = dlib.get_face_chip(img, shape, 150, 0.25)
        vector = facerec.compute_face_descriptor(face_chip)
    except Exception as e:
        logging.error("Exception", exc_info=True)
        return -2, None
    return np.array(vector), scores


def vec_distance(encoding1, encoding2):
    return np.linalg.norm(encoding1 - encoding2)


def verification(pic1_base64, pic2_base64):
    img1 = utils.base64_to_image(pic1_base64)
    img2 = utils.base64_to_image(pic2_base64)
    vector1, score1 = face_encodeing(img1)
    vector2, score2 = face_encodeing(img2)
    # print(vector1)
    # print(vector2)
    print(score1, score2)
    if vector1 is -1 or vector2 is -1:
        return -1
    if vector1 is -2 or vector2 is -2:
        logging.info("图像编码成向量异常")
        return -2
    if score1[0] < 0.1 or score2[0] < 0.1:
        logging.info("图片不够清晰，不能准确定位人脸")
        return -3
    score = (1-vec_distance(vector1, vector2)) * 100 + 20
    if score <= 100:
        return score
    else:
        return score - int(score-99)
