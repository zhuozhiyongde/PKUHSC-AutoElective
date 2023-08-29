#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#@Author  :   Arthals
#@File    :   main.py
#@Time    :   2023/08/27 21:20:43
#@Contact :   zhuozhiyongde@126.com
#@Software:   Visual Studio Code

from .client import ElectiveClient


def run():

    import time
    start = time.time()

    client = ElectiveClient()
    client.start_elective()

    end = time.time()
    print("time cost: ", end - start)
