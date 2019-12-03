# coding=gbk
import os
import sys

# conda cmd:
# pip install sanic
import logging
logging.basicConfig(format='[%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s]: %(message)s',
                    level=logging.INFO)
from sanic import Sanic
from sanic.response import json
import py_eureka_client.eureka_client as eureka_client
from server.verify import *
import yaml
import time


app = Sanic(configure_logging=False)


@app.route('/face_verify/api', methods=["POST"])
async def faceVerify(request):
    get_par = request.json
    if "pic1_base64" not in get_par.keys() or "pic2_base64" not in get_par.keys() not in get_par.keys():
        return json({"result": None, "code": -1, "msg": "field error"})
    pic1_base64 = get_par["pic1_base64"]
    pic2_base64 = get_par["pic2_base64"]
    if type(pic1_base64) != str or type(pic2_base64) != str:
        return json({"result": None, "code": -1, "msg": "field value error"})
    try:
        result = verification(pic1_base64, pic2_base64)
        if result == -1:
            return json({"result": None, "code": -2, "msg": "没有检测到人脸,或者检测到多个人脸"})
        elif result == -2:
            return json({"result": None, "code": -2, "msg": "图像编码成向量异常"})
        elif result == -3:
            return json({"result": None, "code": -2, "msg": "图片不够清晰，不能准确定位人脸"})
    except Exception as e:
        logging.error("Exception", exc_info=True)
        return json({"result": None, "code": -2, "msg": "服务异常"})
    else:
        return json({"similarity": result, "code": 0, "msg": "OK"})


if __name__ == "__main__":
    #eureka_client.init(eureka_server="http://10.194.186.152:8761/eureka/", app_name="video-format-convertion", instance_port=8065, instance_host="127.0.0.1")
    # eureka_client.init(eureka_server="http://10.194.186.152:8761/eureka/",
    #                    app_name="face-verify",
    #                    instance_port=8065)
    app.run(host="0.0.0.0", port=8065)

    # with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")) + '/init.yml') as f:
    #     content = yaml.load(f)
    # eureka_client.init(eureka_server=content["eureka"], app_name="video-cut-face",
    #                    instance_port=content["videoCutFace_port"], instance_host=content["ip"])
    # app.run(host="0.0.0.0", port=content["videoCutFace_port"])
