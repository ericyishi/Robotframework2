#-*- coding: utf-8 -*-
import os
import shutil
import sys

from CusBase import CusBase
class MySelenium(CusBase):
    """
    用户自定义的类
    """

    def __init__(self,
                 running_param,
                 timeout=5.0,
                 implicit_wait=0.0,
                 run_on_failure='capture_page_screenshot',
                 screenshot_root_directory=None
                 ):
        super(MySelenium, self).__init__(running_param,
                                         timeout=5.0,
                                         implicit_wait=0.0,
                                         run_on_failure='capture_page_screenshot',
                                         screenshot_root_directory=None
                                         )
        self.running_param = running_param
        self.browser = self.running_param['BROWSER']
    def copy_drivers_to_local(self):
        """
        将webdriver驱动拷贝到python安装目录下
        :return: True
        """
        python_exe_path = sys.executable #返回python.exe文件的绝对路径，c:\\python27\\python.exe
        python_dir = python_exe_path[0:python_exe_path.rfind(os.sep)]# os.sep根据你所处的平台，自动采用相应的文件的路径，在Windows上是'\'，在Linux上是'/'
        current_dir = os.path.dirname(__file__)
        drivers_src_path = os.path.join(current_dir, '../..', 'TestData\Drivers')
        print drivers_src_path
        drivers = os.listdir(drivers_src_path)# 列出当前路径下的所有文件和文件夹
        for driver in drivers:
            driver_path = os.path.join(drivers_src_path, driver)
            print driver_path
            if os.path.isfile(driver_path):  # 判断是否为文件
                print 'drivers coping, it will take several seconds, please wait……\n %s --> %s' % (driver_path, python_dir)
                shutil.copy2(driver_path, python_dir)
        print 'drivers copy done.'
        return True

if __name__ == '__main__':
    running_param = {
        'BASE_URL': 'http://127.0.0.1:8071/bi/Viewer',
        'BROWSER': 'firefox',
        'DELAY': 1,
    }
    test = MySelenium(running_param,
                      timeout=1.0,
                      implicit_wait=0.0,
                      run_on_failure='capture_page_screenshot',
                      screenshot_root_directory=None
                      )
    test.copy_drivers_to_local()