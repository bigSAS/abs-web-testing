########
Examples
########

.. note::
   I assume that you know basics about how to create Selenium WebDriver instance 👀.
   If not head to `Selenium docs <https://selenium-python.readthedocs.io/getting-started.html#>`_

Examples of using Action Based Framework.   

Basics
######

**Actions** needs **Finder** and Finder needs **WebDriver** so in order to create Actions instance we need to create other objects.

.. code-block:: python

   from selenium import webdriver
   from abswt.elements import FluentFinder
   from abswt.actions import Actions
   from abswt.conditions import XpathExists  # custom expected condition heler class


   driver = webdriver.Chrome()
   finder = FluentFinder(
      driver,
      default_timeout=5  # timeout in seconds, will be passed to WebDriverWait, used for locating WebElements
   )
   actions = Actions(
      finder=finder,
      wait_for_condition_timeout=10,  # timeout in seconds used in .wait_for(condiction)
      wait_between=0.5  # sleep after action time in seconds, triggered after actions like .click(locator_tuple), .type_text(locator_tuple)
   )

   # We're ready for using actions !
   actions.goto('https://mypage.io')
   actions.click(('id', 'some-button-id'))
   actions.wait_for(XpathExists('//div[@id="some-container-id"]'))  # wait for condition (in case page is loading ect.)
   actions.type_text(('name', 'email'), text='foobar')
   actions.submit()
   # etc.

   # WebDriver instance is accesible with .webdriver property
   wd = actions.webdriver
   wd.maximize_window()
   # Finder instance is accesible with .finder property
   fineder = actions.finder
   some_elements = fineder.find_elements(('tag name', 'li'))


With configuration file
#######################

**Good practice** will be keeping configuration values in some kind of config file (defaults can be environment specific)

.. code-block:: json

   {
      "wd_path": "path/to/webderiver",
      "find_element_timeout": 5,
      "wait_for_condition_timeout": 10,
      "wait_between": 0.5
   }

Then in our code  

.. code-block:: python

   import json
   from selenium import webdriver
   from abswt.elements import FluentFinder
   from abswt.actions import Actions


   # class for our config
   @dataclass
   class Config:
      wd_path: str
      find_element_timeout: int
      wait_for_condition_timeout: int
      wait_between: int


   # read config function
   def get_config() -> Config:
      with open('configuration.json', 'r', encoding='utf-8') as c:
         data = json.loads(c.read())
         return Config(**data)

   # usage
   config = get_config()
   driver = webdriver.Chrome(executable_path=config.wd_path)
   finder = FluentFinder(
      driver,
      default_timeout=config.find_element_timeout
   )
   actions = Actions(
      finder=finder,
      wait_for_condition_timeout=config.wait_for_condition_timeout,
      wait_between=config.wait_between
   )
