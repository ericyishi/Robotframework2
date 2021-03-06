#-*- coding: utf-8 -*-
import os

from ImageCompare import ImageCompare
from MySelenium import MySelenium



class CusLibrary(MySelenium,ImageCompare):
    """
    用户自定义的Libraries
    """

    def __init__(self,
                 running_param,
                 timeout=1.0,
                 implicit_wait=0.0,
                 run_on_failure='capture_page_screenshot',
                 screenshot_root_directory=None
                 ):
        super(CusLibrary, self).__init__(running_param,
                                         timeout=1.0,
                                         implicit_wait=0.0,
                                         run_on_failure='capture_page_screenshot',
                                         screenshot_root_directory=None
                                         )
        self.running_param = running_param
if __name__ == '__main__':
    base_path = os.path.dirname(__file__)
    running_param = {
        'BROWSER': 'Chrome',
        'DELAY': 1,
        'BASE_URL': 'https://www.baidu.com/',
        'screenshot_dir': base_path + '/TestData/Screen/Result',
        'expect_picture_dir': base_path + '/TestData/Screen/Expect',
        'result_picture_dir': base_path + '/TestData/Screen/Result',
        'diff_picture_dir': base_path + '/TestData/Screen/Diff'

    }
    test = CusLibrary(running_param,
                      timeout=5.0,
                      implicit_wait=0.0,
                      run_on_failure='Capture Page Screenshot',
                      screenshot_root_directory=None
                      )
    print test.running_param['BROWSER']
    test.open_browser('http://www.baidu.com', 'firefox')
    test.capture_page_screenshot('CusLibrary.png')#截图默认放在当前截图同级目录下