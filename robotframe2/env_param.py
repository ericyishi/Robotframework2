# -*- coding: utf-8 -*-
"""
    和环境绑定的参数文件，传入../TestLibrary。写在一个文件里面方便管理
    :param BROWSER: 浏览器类型, 支持Chrome,ff等
    :param DELAY: 每个Selenium Webdriver命令发送之间的间隔时间,默认单位为秒

"""
import os


base_path = os.path.dirname(__file__)
running_case_para = {
    'BROWSER': 'Chrome',#Chrome|ff
    'DELAY': 0.5,
}

