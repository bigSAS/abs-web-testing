import logging, sys
from abc import ABC
from abswt.actions import Actions


logger = logging.getLogger('abs-page')
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)


class Page(ABC):
    """ Page component base abstraction """
    url = None

    def __init__(self, actions: Actions):
        self.__actions = actions
    
    @property
    def actions(self) -> Actions:
        return self.__actions

    @property
    def title(self):
        return self.__actions.element_provider.driver.title

    def open(self, url: str = None):
        uri = url if url else self.url
        self.actions.goto(uri)
