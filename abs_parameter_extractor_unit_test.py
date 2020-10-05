import unittest
from abs.elements import ParameterExtractor


class ParameterExtractorTest(unittest.TestCase):
    # todo: more tests in for loop for different strings ...
    def test_extract_empty(self):
        text = '/foo[@bar="baz"]'
        e = ParameterExtractor(text)
        params = e.get_parameters()
        assert len(params) == 0
    
    def test_extract_one(self):
        text = '/foo[@bar="{baz}"]'
        e = ParameterExtractor(text)
        params = e.get_parameters()
        assert len(params) == 1
        assert 'baz' in params
    
    def test_extract_two(self):
        text = '/foo[@bar="{baz}-{faz}"]'
        e = ParameterExtractor(text)
        params = e.get_parameters()
        assert len(params) == 2
        assert 'baz' in params
        assert 'faz' in params
    
    def test_extract_three(self):
        text = '/foo[@bar="{baz}-{faz}{gaz}"]'
        e = ParameterExtractor(text)
        params = e.get_parameters()
        assert len(params) == 3
        assert 'baz' in params
        assert 'faz' in params
        assert 'gaz' in params

if __name__ == '__main__':
    unittest.main()
