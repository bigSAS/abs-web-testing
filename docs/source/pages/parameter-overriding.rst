####################
Parameter overriding
####################

Defaults from configuration works good most of the time. But when needed u can override action methods with custom timeout and condition 🖖

Example
#######

.. code-block:: python

    from abswt import expected_conditions as EC  # proxy import for selenium expected conditions

    # find element timeout set to 10 seconds
    actions.click(('id', 'button'), timeout=10)

    # find element with visible condition
    actions.type_text(('name', 'username'), condition=EC.visibility_of_element_located)

    # overide both parameters
    actions.click(('id', 'some-link'), timeout=2, condition=EC.visibility_of_element_located)

