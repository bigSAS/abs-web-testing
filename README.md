# abs-web-testing

Action Based Selenium Web Testing Library.  
Compact Tooling 4 simplier selenium 🥳  

Supports: **Python3.5+**  
Supports: **selenium>=3.141.0**  

Goal: **v1.0** 🤖 (currently working towards v1.0 - API may slightly change 🧠)

Example testing project: [**python-pytest-abs-sample-project**](https://github.com/bigSAS/python-pytest-abs-sample-project)

## Example usage

```python
...
```

Feel free to explore doccumentation at [https://abs-web-testing.readthedocs.io/](https://abs-web-testing.readthedocs.io/)

As for tooday lib is ment to be as barebones as is. And ultra slim.  
If you have any feature requests feel free to issue them on github 👍  

## What is this library ?

Basicly it wraps selenium WebDriver API ino more context based/accessible acion based approach.  
There are 3 main features:  

* abswt.elements.**Locator** - resposible for declaring WebElement locator tuples used by WebDriver  
* abswt.elements.**FluentFinder** - responsible for finding WebElement with batteries included (timeout and condition)  
* abswt.actions.**Actions** - responsible for interacting with WebDriver

Each one of them can be used separately, for your own needs 👌  
Of course they worked great combined toogether (will be explained in **Practical Examples** section ☝️)  

## Instalation

```sh
pip install abs-web-testing
```

## Practical examples

Examples of using ABS.  
I assume that you know basics about how to create Selenium WebDriver instance 👀. If not head to [**selenium docs**](https://selenium-python.readthedocs.io/getting-started.html#).

### Actions basics

**Acions** needs **Finder** and Finder needs **WebDriver** so in order to create Actions instance we need to create other objects.  

```python
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
```

**Good practice** will be keeping configuration values in some kind of config file (defaults can be environment specific)  

#### **configuration.json**

```json
{
    "wd_path": "path/to/webderiver",
    "find_element_timeout": 5,
    "wait_for_condition_timeout": 10,
    "wait_between": 0.5
}
```

### in our codebase

```python
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
    default_timeout=default_timeout=config.find_element_timeout
)
actions = Actions(
    finder=finder,
    wait_for_condition_timeout=config.wait_for_condition_timeout,
    wait_between=config.wait_between
)
```

### Basic with parameter overriding

Even though configuration defaults can be enough most of the times, you can still override action methods with custom timeout and condition 🖖.  

```python
from abswt import expected_conditions as EC  # proxy import for selenium expected conditions


actions.click(('id', 'button'), timeout=10)  # find element timeout set to 10 seconds
actions.type_text(('name', 'username'), condition=EC.visibility_of_element_located)  # find element with visible condition
actions.click(('id', 'some-link'), timeout=2, condition=EC.visibility_of_element_located)  # overide both parameters  
```

### Locator examples

**THE PROBLEM😶**  

Declaring WebElement locator can be painfull. In the end they're nothing else but static strings 🙄.  
Selenium needs *By* and value (str). **By** is also a string. U can see it in Python selenium docs. So all i need is Tuple[str, str] that I can pass to WebDriver methods. Simple right? Yes but ... 🤡  

(**practical example**) Web page has navigation section where there are list elements, that only differ by label.  

```html
<!-- simplified example -->
<ul>
    <li class="menu">Foo</li>
    <li class="menu">Bar</li>
    <li class="menu">Baz</li>
</ul>
```

I want to be able to click each one of them. So the xpath values for them will be:  

```python
foo_xpath = "//ul/li[@class='menu' and contains(., 'Foo')]"
bar_xpath = "//ul/li[@class='menu' and contains(., 'Bar')]"
baz_xpath = "//ul/li[@class='menu' and contains(., 'Baz')]"
```

It can be painfull. Of course **you can write a function** and parametrize the string:  

```python
def get_menu_xpath(label: str):
    return f"//ul/li[@class='menu' and contains(., '{label}')]"
```

**But then you'll end up with more functions, more parameters, more complex implementation**🤒  

**abswt.elements.Locator** is the solution 🤯 It provides handy way of hanling parameterized selectors, and of course includes simple standard ones.  

```python
from abswt.elements import Locator, Using # using is the same as By

# simple clasic static locator
simple_button = Locator(Using.ID, 'button')
simple_button.get_by()
# >>> ('id', 'button')
simple_button.is_parameterized
# False
simple_button.parameters
# []

# parameterized button
foo_action_button = Locator(Using.NAME, 'action-{foo}')
foo_action_button.get_by(foo='foo')
# >>> ('name', 'action-foo')
foo_action_button.get_by(foo='foobar')
# >>> ('name', 'action-foobar')
simple_button.is_parameterized
# True
simple_button.parameters
# ['foo']

# You can define many parameters
menu_element = Locator(Using.XPATH, "//ul/li[@class='{class_name}' and contains(., '{label}')]")
menu_element.get_by(class_name='menu', label='Foo')
# >>> ("xpath", "//ul/li[@class='menu' and contains(., 'Foo')]")
menu_element.get_by(class_name='active-menu', label='Bar')
# >>> ("xpath", "//ul/li[@class='active-menu' and contains(., 'Bar')]")
```

All you need to remeber is to pass parameters into **get_by** using **keyword arguments** with the same names as defined in value template 🧠.  
Cool stuff.  
**Locator validates if the parameter has been passed to get_by. When not passed it will raise ValueError 🤖**  

```python
button = Locator(Using.NAME, '{action}-{foo}')
button.get_by()
# ValueError: get_by method is missing keyword arguments: ['action', 'foo']
button.get_by(action='goto')
# ValueError: get_by method is missing keyword argument: foo
```

### Page Object Pattern examples

**abswt.pages.Page** is basic abstraction for defining Page Object Classes.  
It provides access to Actions with .actions parameter.  

Example Page Object class:  

```python
class SasKodzi(Page):
    url = 'https://sas-kodzi.pl'

    BLOG_BUTTON = Locator(Using.XPATH, '//a[@href="/blog"]')
    POST_BUTTON = Locator(Using.XPATH, "//section[@class='blog-post' and contains(., '{post_title}')]//a[contains(., 'Czytaj')]")

    def goto_posts(self) -> None:
        self.actions.click(self.BLOG_BUTTON.get_by())

    def open_post(self, post_title: str) -> None:
        self.actions.click(self.POST_BUTTON.get_by(post_title=post_title), condition=EC.visibility_of_element_located)


# usage
page = SasKodzi(actions)
page.open()
page.goto_posts()
page.open_post('some title')
```

### Finder

**abswt.elements.Finder** its an abstraction needed for action framewrok. Interpreted as an inteface for finding WebElements.  
U can use abswt.elements.**FluentFinder** or implement your own to suite your own needs 🧠.  

```python
from abswt.elements import FluentFinder


# basic usage
finder = FluentFinder(driver, 5)
button = finder.find_element(('id', 'button'))  # single WebElement
options = finder.find_elemens('tag name', 'option')  # many WebElements
```  

Custom Finder examples  

```python
from abswt.elements import Finder, FluentFinder
from abswt import expected_conditions as EC


# custom FluentFinder
# FluentFinder defaut conditions are -> elements must be present
class VisibleFluentFinder(FluentFinder):
    # my default condtitions -> elements must be visible
    default_single_condition = EC.visibility_of_element_located
    default_multi_condition = EC.visibility_of_all_elements_located

#custom Finder
class SimpleFinder(Finder):
    # most basic WebElement finder (dont use it like that 💀)

    def find_element(self, locator_tuple: tuple, timeout: int = None, condition: object = None) -> WebElement:
        return self.webdriver.find_element(**locator_tuple)

    def find_elements(self, locator_tuple: tuple, timeout: int = None, condition: object = None) -> WebElement:
        return self.webdriver.find_elements(**locator_tuple)
```

I hope You'll get the idea 👍  

### PyTest

## Logging

## API

### abswt.elements.**Locator**

todo

### abswt.elements.**FluentFinder**

todo

### abswt.actions.**Actions**

todo

## Run unit tests

```sh
python abs_tests.py
```
