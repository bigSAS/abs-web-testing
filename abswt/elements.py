import logging, sys
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional, Tuple

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver


class Using(Enum):
    """ Enum for locator types, same as selenium By """
    ID = "id"
    NAME = "name"
    XPATH = "xpath"
    CLASS = "class name"
    CSS = "css selector"
    TAG_NAME = "tag name"
    LINK_TEXT = "link text"
    PARTIAL_LINK_TEXT = "partial link text"


class ParameterExtractor:
    """ Extract {param} parameters from str """
    def __init__(self, text: str) -> None:
        self.__text = text
    
    def get_parameters(self) -> List[str]:
        # todo: refactor ?
        params = []
        param, last_index = self.__find_param(start_index=0)
        while param is not None and last_index > -1:
            params.append(param)
            param, last_index = self.__find_param(start_index=last_index)
        return params
    
    def __find_param(self, start_index: int) -> Tuple[Optional[str], int]:
        # todo: refactor ?
        open = self.__text.find('{', start_index)
        close = self.__text.find('}', start_index + 1)
        if open == -1 or close == -1:
            return None, -1
        if open > close:
            return None, -1
        return self.__text[open + 1:close], close


class Locator:
    """
    Represents WebElement Locator with some extra goodies
    
    Example usage:
    Traditional static locator tuple:
    
    button = Locator(Using.XPATH, '//button')
    # get locator tuple:
    button.get_by()

    
    Goodies:
    Parameterized locator tuple:
    
    parameterized_button = Locator(Using.XPATH, '//button[@name="{button_name}"]')
    foo_by = parameterized_button.get_by(button_name='foo')  # -> ('xpath', '//button[@name="foo"]'
    bar_by = parameterized_button.get_by(button_name='bar')  # -> ('xpath', '//button[@name="bar"]'
    # ! parameters in curly brackets must be passed as keyword arguments into get_by method !
    When forgoten to pass parameters you will get an error:
    parameterized_button.get_by()
    >>> ValueError: get_by method is missing keyword arguments: ['button_name']'
    or
    >>> ValueError: get_by method is missing keyword argument: button_name

    For more examples head to README.md / docs :)
    
    """
    def __init__(self, using: Using, value: str, parameter_extractor: ParameterExtractor = None) -> None:
        self.__using = using
        self.__value = value
        self.__parameter_extractor = parameter_extractor if parameter_extractor else ParameterExtractor(self.__value)
    
    @property
    def using(self) -> Using:
        return self.__using
    
    @property
    def value(self) -> str:
        return self.__value

    @property
    def parameters(self) -> List[str]:
        return self.__parameter_extractor.get_parameters()

    @property
    def is_parameterized(self) -> bool:
        return len(self.parameters) > 0


    def get_by(self, **kwargs) -> Tuple[str, str]:
        """ get (by, value) tuple for finding selenium WebElement object """
        return (self.using.value, self.__get_value(**kwargs))

    def __get_value(self, **kwargs) -> str:
        if self.is_parameterized:
            return self.__parameterize_value(**kwargs)
        return self.value
    
    
    def __parameterize_value(self, **kwargs) -> str:
        if len(kwargs.keys()) == 0: raise ValueError(f'get_by method is missing keyword arguments: {self.parameters}')
        self.__validate_parameters(**kwargs)
        return self.value.format(**kwargs)
    
    def __validate_parameters(self, **kwargs):
        for param in self.parameters:
            if param not in kwargs.keys():
                raise ValueError(f'get_by method is missing keyword argument: {param}')


class Finder(ABC):
    """
    Abstraction for finding WebElements
    
    Basic implementation in abs.elements.FluentFinder
    """

    def __init__(self, webdriver: WebDriver) -> None:
        self.__webdriver = webdriver
        logger = logging.getLogger('abs-finder')
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)
        self.logger = logger
        self.logger.setLevel(logging.DEBUG)

    @property
    def webdriver(self) -> WebDriver:
        return self.__webdriver
    
    @abstractmethod
    def find_element(self, locator_tuple: tuple, timeout: int = None, condition: object = None) -> WebElement:
        pass

    @abstractmethod
    def find_elements(self, locator_tuple: tuple, timeout: int = None, condition: object = None) -> List[WebElement]:
        pass


class FluentFinder(Finder):
    """
    Default Finder implementation. Should be usefull for most web testing use cases :)

    Example usage:
    finder = FluenFinder(webdriver, default_timeout = 5)

    default_timeout -> is the default WebDriverWait timeout for finding WebElement -> it can be overriden in both of finder methods
    default_single_condition -> default WebDriverWait condition for finding single WebElement -> it can be overriden in both of finder methods
    default_multi_condition -> same as above, except for finding multiple WebElements
    """
    default_single_condition = EC.presence_of_element_located
    default_multi_condition = EC.presence_of_all_elements_located

    def __init__(self, webdriver: WebDriver, default_timeout: int) -> None:
        self.default_timeout = default_timeout
        super().__init__(webdriver)

    def find_element(self, locator_tuple: tuple, timeout: int = None, condition: object = None) -> WebElement:
        t = timeout if timeout else self.default_timeout
        c = condition if condition else self.default_single_condition
        self.logger.debug(f'find_element: {locator_tuple}, timeout: {t} sec, condition: {c}')
        return WebDriverWait(self.webdriver, t).until(c(locator_tuple))

    def find_elements(self, locator_tuple: tuple, timeout: int = None, condition: object = None) -> WebElement:
        t = timeout if timeout else self.default_timeout
        c = condition if condition else self.default_multi_condition
        self.logger.debug(f'find_elements: {locator_tuple}, timeout: {t} sec, condition: {c}')
        return WebDriverWait(self.webdriver, t).until(c(locator_tuple))
