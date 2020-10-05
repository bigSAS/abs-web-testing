from abs.elements import Locator, Using
import unittest


class LocatorTests(unittest.TestCase):
    """ Locator class tests """

    def test_construct(self):
        locator = Locator(using=Using.ID, value='foo')
        assert locator.using == Using.ID
        assert locator.using.value == 'id'
        assert locator.value == 'foo'

    def test_non_parameterized(self):
        locator = Locator(using=Using.XPATH, value='//foo[@bar="baz"]')
        assert locator.is_parameterized == False
        assert locator.get_by() == ('xpath', '//foo[@bar="baz"]')
    
    def test_parameterized(self):
        locator = Locator(using=Using.XPATH, value='//foo[@bar="{baz}"]//jimmy[{choo}]')
        assert locator.is_parameterized == True
        parameters = locator.parameters
        assert 'baz' in parameters
        assert 'choo' in parameters
        parmeterized = locator.get_by(baz='a', choo='b')
        expected_value = '//foo[@bar="a"]//jimmy[b]'
        assert parmeterized == ('xpath', expected_value)
    
    def test_parmeterization_erros(self):
        pass  # todo: impl -> check exception raising ...

if __name__ == '__main__':
    unittest.main()
