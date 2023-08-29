#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#@Author  :   Arthals
#@File    :   const.py
#@Time    :   2023/08/27 09:11:12
#@Contact :   zhuozhiyongde@126.com
#@Software:   Visual Studio Code

import os


def get_abs_path(*path):
    return os.path.normpath(
        os.path.abspath(os.path.join(os.path.dirname(__file__), *path)))


CONFIG_INI = get_abs_path('../config.ini')
CAPTCHA_PATH = get_abs_path('../captcha')


class ElectiveURL(object):
    '''
    Host        主域名
    '''
    Scheme = 'https'
    Host = 'xsxk.bjmu.edu.cn'
    VCode = 'https://xsxk.bjmu.edu.cn/xsxkapp/sys/xsxkapp/student/4/vcode.do'
    Captcha = 'https://xsxk.bjmu.edu.cn/xsxkapp/sys/xsxkapp/student/vcode/image.do'
    Login = 'https://xsxk.bjmu.edu.cn/xsxkapp/sys/xsxkapp/student/check/login.do'
    Batch = 'https://xsxk.bjmu.edu.cn/xsxkapp/sys/xsxkapp/elective/batch.do'
    Choose = 'https://xsxk.bjmu.edu.cn/xsxkapp/sys/xsxkapp/elective/volunteer.do'
    Withdraw = 'https://xsxk.bjmu.edu.cn/xsxkapp/sys/xsxkapp/elective/deleteVolunteer.do'
    PublicCourse = "https://xsxk.bjmu.edu.cn/xsxkapp/sys/xsxkapp/elective/programCourse.do"