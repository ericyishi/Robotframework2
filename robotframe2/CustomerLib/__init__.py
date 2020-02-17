#-*- coding: utf-8 -*-
import os
import sys
from CusLibrary import CusLibrary


class CustomerLib(CusLibrary):
    """
    TestLibrary class, include all the methods
    """

    def __init__(self,
                 running_param,
                 timeout=1.0,
                 implicit_wait=0.0,
                 run_on_failure='capture_page_screenshot',
                 screenshot_root_directory=None
                 ):
        super(CustomerLib, self).__init__(running_param,
                                          timeout=1.0,
                                          implicit_wait=0.0,
                                          run_on_failure='capture_page_screenshot',
                                          screenshot_root_directory=None
                                          )
        current_dir = os.path.dirname(__file__)
        print "current_dir:"+current_dir # D:/yishi/git/robotframework/robotframe2/CustomerLib
        sys.path.append(current_dir[:current_dir.find('CustomerLib')]) #放入到sys.path里面
        # current_dir[:current_dir.find('TestLibrary')] 先返回TestLibrary的索引，然后使用切片反向获取TestLibrary之前路径
        print current_dir[:current_dir.find('CustomerLib')]# D:/yishi/git/robotframework/robotframe2/
        print sys.path
        env_module = __import__('env_param') #动态引入env_param模块
        self.running_param = getattr(env_module, 'running_case_para')

if __name__ == '__main__':
    running_param = {
        'BROWSER': 'Chrome',
        'DELAY': 1,
    }
    test = CustomerLib(running_param,
                       timeout=5.0,
                       implicit_wait=0.0,
                       run_on_failure='Capture Page Screenshot',
                       screenshot_root_directory=None
                       )
    # print test.running_param['DB']
    # print test.running_param['BASE_URL']
    # print test.running_param['screenshot_dir']
    print test.running_param['BROWSER']
    test.open_browser('http://www.baidu.com', test.running_param['BROWSER'])
    test.capture_page_screenshot('TestLibrary.png')
    test.close_browser()