import logging, sys
from time import sleep
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from abs.elements import Finder


logger = logging.getLogger('abs-actions')
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

class Actions:
    """ ... """
    # todo: docstring

    def __init__(self, finder: Finder,  wait_for_condition_timeout: int, wait_between: int = 0) -> None:
        self.wait_between_sec = wait_between
        self.wait_for_condition_timeout = wait_for_condition_timeout
        self.__finder = finder

    @property
    def webdriver(self) -> WebDriver:
        return self.finder.webdriver
    
    @property
    def finder(self) -> Finder:
        return self.__finder
    
    def goto(self, url: str) -> None:
        logger.info(f'goto:: {url}')
        self.webdriver.get(url)
    
    def click(self, locator_tuple: tuple, timeout: int = None, condition: object = None) -> None:
        logger.info(f'click:: {locator_tuple}')
        self.finder.find_element(locator_tuple, timeout, condition).click()
        self.sleep()
        
    def type_text(self, locator_tuple: tuple, text: str, timeout: int = None, condition: object = None) -> None:
        logger.info(f'type text:: {locator_tuple}')
        self.finder.find_element(locator_tuple, timeout, condition).send_keys(text)
        self.sleep()
    
    def submit(self, locator_tuple: tuple = None, timeout: int = None, condition: object = None) -> None:
        lt = locator_tuple if locator_tuple else ('xpath', '//form')
        logger.info(f'submit:: {lt}')
        self.finder.find_element(lt, timeout, condition).submit()
        self.sleep()

    def wait_for(self, condition: object, timeout: int = None) -> None:
        t = timeout if timeout else self.wait_for_condition_timeout
        logger.info(f'wait for:: {condition}, timeout: {t} sec')
        WebDriverWait(self.webdriver, t).until(condition)

    def get_attribute(self, locator_tuple: tuple, attr: str, timeout: int = None, condition: object = None) -> str:
        logger.info(f'get attribute:: {locator_tuple} [{attr}]')
        return self.finder.find_element(locator_tuple, timeout, condition)\
            .get_attribute(attr)

    def get_text(self, locator_tuple: tuple, timeout: int = None, condition: object = None) -> str:
        return self.get_attribute(locator_tuple, 'innerText', timeout, condition)
    
    def execute_js(self, js_script: str) -> str:
        logger.info(f'execute js::\n{js_script}')
        return str(self.webdriver.execute_script(js_script))

    def sleep(self, sec: int = None):
        seconds = sec if sec else self.wait_between_sec
        logger.debug(f'sleep:: {seconds} sec')
        sleep(seconds)
