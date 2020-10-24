import logging, sys
from time import sleep
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from abswt.elements import Finder


logger = logging.getLogger('abs-actions')
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

class Actions:
    """
    Action - responsible for webdriver operations:
    - finding elements
    - clicking, typing, submiting etc...

    Parameters:
    finder:  abs.elements.Finder instance (u can use abs.elements.FluentFinder or implement your own :) )
    wait_for_condition_timeout: default wait for condition timeout when using wait_for method
    wait_between: default delay between action method calls, defaults 0sec

    WebDriver and Finder are accessible with properties .webdriver and .finder

    Action methods are preety self explanotary :)
    Most action methods can override timeout (find WebElement timeout) and condition (expected condition for finding WebElement).
    For readability purpouses they should be used as keyword arguments(timeout, condition)

    Example usage:
    finder = FluenFinder(webdriver, default_timeout=5)
    actions = Actions(finder, wait_for_condition_timeout=10, wait_between=1)

    actions.goto(url)
    actions.click(locator)
    actions.click(locator, timeout=10)
    actions.click(locator, condition=EC.visibility_of_element_located)

    For more practical examples check out README.md / docs

    The actions.<method>(locator_tuple: tuple) -> classic tuple for selenium webriver methods ex: ('xpath', '//div/form') or ('id', 'foobar')

    For helpful and super handy selector tuple implementation check out abs.elements.Locator documentation :) and examples in README.md / docs
    """
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
        
    def clear_field(self, locator_tuple: tuple, timeout: int = None, condition: object = None) -> None:
        logger.info(f'clear field:: {locator_tuple}')
        self.finder.find_element(locator_tuple, timeout, condition).clear()
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
    
    def hover(self, locator_tuple: tuple, timeout: int = None, condition: object = None) -> None:
        logger.info(f'hover element:: {locator_tuple}')
        element = self.finder.find_element(locator_tuple, timeout, condition)
        ActionChains(self.webdriver).move_to_element(element).perform()
        self.sleep()
        
    def sleep(self, sec: int = None):
        seconds = sec if sec else self.wait_between_sec
        logger.debug(f'sleep:: {seconds} sec')
        sleep(seconds)
