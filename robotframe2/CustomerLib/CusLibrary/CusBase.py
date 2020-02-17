#-*- coding: utf-8 -*-
import os

from Selenium2Library import Selenium2Library
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from robot.libraries.BuiltIn import BuiltIn
class CusBase(Selenium2Library):
    def __init__(self,
                 running_param,
                 timeout=5.0,
                 implicit_wait=0.0,
                 run_on_failure='capture_page_screenshot',
                 screenshot_root_directory=None
                 ):
        self._builtin = BuiltIn()
        super(CusBase, self).__init__(timeout=5.0,
                                      implicit_wait=0.0,
                                      run_on_failure='capture_page_screenshot',
                                      screenshot_root_directory=None
                                      )
        self.running_param = running_param

    def send_keywords(self, *keywords):
        """send keys to locator
        :param keywords:keys to send
        调用Input Text会先Click Element,导致Ctrl_A失效，因此新增该方法
        """
        ActionChains(self._current_browser()).send_keys(*keywords).perform()
        return self
    def right_click(self, locator=None):
        """right click on element identified by `locator`.
        If None, clicks on current mouse position.
        """
        if locator:
            element = self._element_find(locator, True, True)
            ActionChains(self._current_browser()).context_click(element).perform()
            return self
        else:
            ActionChains(self._current_browser()).context_click(locator).perform()
            return self

if __name__ == '__main__':
    base_path = os.path.dirname(__file__)
    running_param = {
        'BROWSER': 'chrome',
        'DELAY': 1
    }
    test = CusBase(running_param,
                   timeout=1.0,
                   implicit_wait=0.0,
                   run_on_failure='capture_page_screenshot',
                   screenshot_root_directory=None
                   )
    # print test.running_param['BROWSER']
    test.open_browser('http://www.baidu.com', test.running_param['BROWSER'])