from selenium.webdriver.remote.webdriver import WebDriver

"""
Expected conditions:

To implement your own expected condition, selenium expects from you object with a __call__ implementation.
Its good to remembet that selenium allways pasess WebDriver instance into __call__ method :)
"""

class XpathExists:
    """
    Wait for xpath to exist
    """
    def __init__(self, xpath: str):
        self.__xpath = xpath

    # noinspection PyBroadException
    def __call__(self, driver: WebDriver):
        try:
            driver.find_element_by_xpath(self.__xpath)
            return True
        except:
            return False

    def __str__(self):
        return f'xpath-exists -> {self.__xpath}'

    def __repr__(self):
        return self.__str__()
