##########
Quickstart
##########

Disclaimer
##########

As for tooday lib is ment to be as barebones as is. And ultra slim.  
If you have any feature requests feel free to issue them on github 👍  

What is this library ?
######################

Basicly it wraps selenium WebDriver API ino more context based/accessible acion based approach.  
There are 3 main features:  

* abswt.elements.Locator - resposible for declaring WebElement locator tuples used by WebDriver  
* abswt.elements.FluentFinder - responsible for finding WebElement with batteries included (timeout and condition)  
* abswt.actions.Actions - responsible for interacting with WebDriver

Each one of them can be used separately, for your own needs 👌  
Of course they worked great combined toogether (will be explained in **Practical Examples** section ☝️)  

.. note::
   As for tooday lib is ment to be as barebones as is. And ultra slim.
   If you have any feature requests feel free to issue them on github 👍


Instalation
###########

.. code-block:: sh
   
   pip install abs-web-testing
