#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#@Author  :   Arthals
#@File    :   notifier.py
#@Time    :   2023/09/18 00:14:02
#@Contact :   zhuozhiyongde@126.com
#@Software:   Visual Studio Code

import requests
from .config import ElectiveConfig


class BarkNotifier():

    def __init__(self):
        self._config = ElectiveConfig()
        self._bark_key = self._config.bark_key

    def notify_success(self, title, content):
        if not self._bark_key:
            return
        try:
            requests.get(
                f"https://api.day.app/{self._bark_key}/",
                params={
                    'title': title,
                    'icon':
                    'https://cdn.arthals.ink/bed/2023/09/5b213e501ef956ea8c4bdf7e3e42489b.png',
                    'body': content,
                })
        except Exception as e:
            print(e)

    def notify_fail(self, title, content):
        if not self._bark_key:
            return
        try:
            requests.get(
                f"https://api.day.app/{self._bark_key}/",
                params={
                    'title': title,
                    'icon':
                    'https://cdn.arthals.ink/bed/2023/09/dc5e647c618cc0bef54921c566b48517.png',
                    'body': content
                })
        except Exception as e:
            print(e)
