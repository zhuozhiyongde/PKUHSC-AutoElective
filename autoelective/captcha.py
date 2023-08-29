#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#@Author  :   Arthals
#@File    :   captcha.py
#@Time    :   2023/08/27 21:14:06
#@Contact :   zhuozhiyongde@126.com
#@Software:   Visual Studio Code

from .config import ElectiveConfig
import base64
import json
import requests


class Captcha():
    _RECONGNIZER_URL = "http://api.ttshitu.com/base64"

    def __init__(self):
        self._config = ElectiveConfig()

    def recongnize(self, raw):
        _type_id = 13
        # raw: 16进制字符串
        # 转换为base64
        base64_data = base64.b64encode(raw).decode('utf-8')
        # 发送请求
        data = {
            'username': self._config.captcha_username,
            'password': self._config.captcha_password,
            'typeid': _type_id,
            'image': base64_data
        }
        try:
            resp = requests.post(self._RECONGNIZER_URL, json=data, timeout=20)
            if resp.status_code == 200:
                res = json.loads(resp.text)
                print("ocr result: ", res["data"]["result"])
                return res["data"]["result"]

        except Exception as e:
            print(e)
            return None
