#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#@Author  :   Arthals
#@File    :   client.py
#@Time    :   2023/08/27 09:21:18
#@Contact :   zhuozhiyongde@126.com
#@Software:   Visual Studio Code

from requests.models import Request
from requests.sessions import Session
import time
import json
import os
import re
import base64
from .const import ElectiveURL
from .config import ElectiveConfig


class ElectiveClient():

    default_headers = {}
    default_headers[
        'Accept'] = 'application/json, text/javascript, */*; q=0.01'
    default_headers['Accept-Encoding'] = 'gzip, deflate, br'
    default_headers['Accept-Language'] = 'zh-CN,zh;q=0.9'
    default_headers['Connection'] = 'keep-alive'
    default_headers[
        'Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    default_headers['Host'] = 'xsxk.bjmu.edu.cn'
    default_headers[
        'User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    default_headers["Sec-Fetch-Dest"] = "empty"
    default_headers["Sec-Fetch-Mode"] = "cors"
    default_headers["Sec-Fetch-Site"] = "same-origin"

    def __init__(self):
        self._config = ElectiveConfig()
        self._session = Session()
        self._session.headers.update(self.__class__.default_headers)
        self.get_vtoken()
        self.get_batch()

    def _request(self,
                 method,
                 url,
                 params=None,
                 data=None,
                 headers=None,
                 cookies=None,
                 auth=None,
                 json=None):
        req = Request(method=method.upper(),
                      url=url,
                      headers=headers,
                      data=data or {},
                      json=json,
                      params=params or {},
                      auth=auth,
                      cookies=cookies)
        prep = self._session.prepare_request(req)
        prep._client = self

        resp = self._session.send(prep, timeout=5)

        # print(prep.url)

        return resp

    def _get(self, url, params=None, **kwargs):
        return self._request('GET', url, params=params, **kwargs)

    def _post(self, url, data=None, json=None, **kwargs):
        return self._request('POST', url, data=data, json=json, **kwargs)

    def _update_headers(self, **kwargs):
        self._session.headers.update(**kwargs)

    def get_vtoken(self):
        r = self._get(ElectiveURL.VCode + f"?{int(time.time() * 1000)}")
        self.vtoken = r.json()['data']['token']

    def get_captcha(self):
        from .const import CAPTCHA_PATH

        if (not os.path.exists(CAPTCHA_PATH)):
            os.mkdir(CAPTCHA_PATH)

        r = self._get(ElectiveURL.Captcha, {
            "vtoken": self.vtoken,
        })

        with open(CAPTCHA_PATH + '/captcha.jpg', 'wb') as f:
            f.write(r.content)

        return r.content

    def ocr_captcha(self):
        from .captcha import Captcha
        captcha = Captcha()
        return captcha.recongnize(self.get_captcha())

    def try_login(self):
        import execjs

        with open('./autoelective/encrypt.js', 'r') as f:
            script = f.read()

        ctx = execjs.compile(script)
        res = ctx.call('strEnc', self._config.password, "this", "password",
                       "is")

        data = {
            "timestrap": int(time.time() * 1000),
            "loginName": self._config.username,
            "loginPwd": base64.b64encode(res.encode('utf-8')).decode('utf-8'),
            "verifyCode": self.ocr_captcha(),
            "vtoken": self.vtoken
        }

        r = self._get(ElectiveURL.Login, data)

        try:
            res_cookies = r.headers['Set-Cookie']
            jsessionid = re.search('JSESSIONID=.*?(?=;)', res_cookies).group()
            weu = re.search('_WEU=.*?(?=;)', res_cookies).group()
            update_cookies = f"{weu}; {jsessionid}"

            self._update_headers(Cookie=update_cookies)

            r = r.json()

            if r['msg'] == '登录成功':
                self.token = r['data']['token']
                self._update_headers(Token=self.token)
                print("login success")
                print(f" - [username]: {self._config.username}")
                # print("token is: ", self.token)

            else:
                raise Exception(r['msg'])

        except Exception as e:
            print(f"[LOGIN ERROR]: {e}")
            raise Exception("login failed")

    def login(self):
        max_retry = 10
        while max_retry > 0:
            try:
                self.try_login()
                return
            except Exception as e:
                print(f"[OCR ERROR]: {e}")
                max_retry -= 1
                self.get_vtoken()
                time.sleep(1)

    def get_batch(self):
        r = self._get(ElectiveURL.Batch, {
            "timestamp": int(time.time() * 1000),
        })
        r = r.json()['dataList']

        # 找到 name 为 batch_name 的 batch
        for batch in r:
            if batch['name'] == self._config.batch_name:
                self._batch_info = batch
                # 可以检索一下时间是否符合要求
                return

        raise Exception("batch not found")

    def choose_course(self, teachingClassId, teachingClassType):
        addParam = {
            "data": {
                "operationType": "1",
                "studentCode": self._config.username,
                "electiveBatchCode": self._batch_info['code'],
                "teachingClassId": str(teachingClassId),
                "isMajor": "1",
                "campus": "1",
                "teachingClassType": str(teachingClassType),
            }
        }

        r = self._post(
            ElectiveURL.Choose,
            data={"addParam": json.dumps(addParam, separators=(',', ':'))})

        try:
            r = r.json()
            if r['code'] == '1':
                print(f" - [choose] success: {teachingClassId}")
                return
            raise Exception(r['msg'])
        except Exception as e:
            print(f"[CHOOSE ERROR]: {e}")

    def withdraw_course(self, teachingClassId):
        deleteParam = {
            "data": {
                "operationType": "2",
                "studentCode": self._config.username,
                "electiveBatchCode": self._batch_info['code'],
                "teachingClassId": str(teachingClassId),
                "isMajor": "1",
            }
        }
        r = self._get(
            ElectiveURL.Withdraw,
            {
                "timestamp": int(time.time() * 1000),
                "deleteParam": json.dumps(deleteParam, separators=(',', ':'))
            },
        )
        # {"data":null,"code":"1","msg":"删除选课志愿成功","timestamp":"2","map":null}
        try:
            r = r.json()
            if r['code'] == '1':
                print(f" - [withdraw] success: {teachingClassId}")
                return
            raise Exception(r['msg'])
        except Exception as e:
            print(f"[WITHDRAW ERROR]: {e}")

    def start_elective(self):
        begin_time = self._batch_info['beginTime']
        # 转化为时间戳
        begin_time = time.mktime(time.strptime(begin_time,
                                               "%Y-%m-%d %H:%M:%S"))
        if (begin_time - time.time() > 0):
            print("waiting:", int(begin_time - time.time()), "s")
            time.sleep(begin_time - time.time())

        self.login()
        for course_id, course_config in self._config.courses.items():
            print("current: ", course_id)
            if 'conflict' in course_config:
                self.withdraw_course(course_config['conflict'])
            self.choose_course(course_config['class'], course_config['type'])
