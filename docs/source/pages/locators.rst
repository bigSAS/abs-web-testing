########
Locators
########

The problem
###########

Declaring WebElement locator can be painfull. In the end they're nothing else but static strings 🙄.
Selenium needs **By** and value (str). **By** is also a string. U can see it in Python selenium docs.
So all i need is Tuple[str, str] that I can pass to WebDriver methods. Simple right? Yes but ... 🤡
For example - web page has navigation section where there are list elements, that only differ by label.

.. code-block:: html

    <ul>
        <li class="menu">Foo</li>
        <li class="menu">Bar</li>
        <li class="menu">Baz</li>
    </ul>

I want to be able to click each one of them. So the xpath values for them will be:

.. code-block:: python

    foo_xpath = "//ul/li[@class='menu' and contains(., 'Foo')]"
    bar_xpath = "//ul/li[@class='menu' and contains(., 'Bar')]"
    baz_xpath = "//ul/li[@class='menu' and contains(., 'Baz')]"

It can be painfull. Of course **you can write a function** and parametrize the string

.. code-block:: python

    def get_menu_xpath(label: str):
        return f"//ul/li[@class='menu' and contains(., '{label}')]"

But then you'll end up with **more functions, more parameters, more complex** implementation🤒

**abswt.elements.Locator** is the solution 🤯 It provides handy way of hanling parameterized selectors, and of course includes simple standard ones.


The Locator class
#################

Locator provides simple api for managing selenium locators.

Example:

.. code-block:: python

    from abswt.elements import Locator, Using


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

All you need to remeber is to pass parameters into **get_by** using **keyword arguments** with the same names as defined in value template 🧠.

Cool stuff.

Validation
##########

Locator validates if the parameter has been passed to get_by. When not passed it will raise ValueError 🤖

.. code-block:: python

    button = Locator(Using.NAME, '{action}-{foo}')
    button.get_by()
    # ValueError: get_by method is missing keyword arguments: ['action', 'foo']
    button.get_by(action='goto')
    # ValueError: get_by method is missing keyword argument: foo

Locators in Page Object Pattern
###############################

**abswt.pages.Page** is basic abstraction for defining Page Object Classes.
It provides access to Actions with .actions parameter.

.. code-block:: python
    
    from abswt import expected_conditions as EC  # proxy import for selenium expected conditions


    class SasKodzi(Page):
        url = 'https://sas-kodzi.pl'

        BLOG_BUTTON = Locator(Using.XPATH, '//a[@href="/blog"]')
        POST_BUTTON = Locator(Using.XPATH, "//section[@class='blog-post' and contains(., '{post_title}')]//a[contains(., 'Czytaj')]")

        def goto_posts(self) -> None:
            self.actions.click(self.BLOG_BUTTON.get_by())

        def open_post(self, post_title: str) -> None:
            self.actions.click(self.POST_BUTTON.get_by(post_title=post_title), condition=EC.visibility_of_element_located)

Then use page object

.. code-block:: python

    page = SasKodzi(actions)
    page.open()
    page.goto_posts()
    page.open_post('some title')

