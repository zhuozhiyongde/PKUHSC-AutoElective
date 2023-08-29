#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#@Author  :   Arthals
#@File    :   config.py
#@Time    :   2023/08/27 09:10:24
#@Contact :   zhuozhiyongde@126.com
#@Software:   Visual Studio Code

from .const import CONFIG_INI
from configparser import RawConfigParser
import re


class ElectiveConfig():

    def __init__(self):
        self._config = RawConfigParser()
        self._config.read(CONFIG_INI, encoding='utf-8')

    @property
    def username(self):
        return self._config.get('elective', 'username')

    @property
    def password(self):
        return self._config.get('elective', 'password')

    @property
    def batch_name(self):
        return self._config.get('elective', 'batch_name')

    @property
    def captcha_username(self):
        return self._config.get('captcha', 'username')

    @property
    def captcha_password(self):
        return self._config.get('captcha', 'password')

    @property
    def courses(self):
        cs = {}
        for section in self._config.sections():
            if re.match(r"course:", section):
                course_id = section.split(":")[1]
                for k, v in self._config.items(section):
                    cs.setdefault(course_id, {})[k] = v
        return cs
