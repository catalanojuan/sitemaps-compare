
from mock import patch, Mock
from unittest import TestCase

from sitemaps_compare import compare

class SitemapsCompareTestCase(TestCase):

    def setUp(self):
        """
        This mocks the get call to requests, returning a Mock instance that
        will answer to the content attr with the content of the xml file
        specified in the URL.
        """
        self.get_mock = lambda url: Mock(
                    content=open(
                        'xmls/{url}'.format(url=url[len('http://domainN.com/'):]), 
                        'r'
                    ).read()
                )

    @patch('sitemaps_compare.requests')
    def test_equal_one_level_same_order(self, requests_mock):
        """
        Tests the simplest case: only one level in the XML tree, same leaves.
        Should return True.
        """
        requests_mock.get = self.get_mock
        self.assertTrue(compare('http://domain1.com/example1.xml', 'http://domain2.com/example1.xml'))

    @patch('sitemaps_compare.requests')
    def test_equal_one_level_diff_order(self, requests_mock):
        """
        Tests the case: only one level in the XML tree, same leaves but in different order.
        Should return True.
        """
        requests_mock.get = self.get_mock

        self.assertTrue(compare('http://domain1.com/example1.xml', 'http://domain2.com/example2.xml'))
    
    @patch('sitemaps_compare.requests')
    def test_not_equal_first_level_different(self, requests_mock):
        """
        Tests the case: only one level in the XML tree, different leaves.
        Should return False.
        """
        requests_mock.get = self.get_mock

        self.assertFalse(compare('http://domain1.com/example1.xml', 'http://domain3.com/example3.xml'))

    @patch('sitemaps_compare.requests')
    def test_equal_two_levels_equal(self, requests_mock):
        """
        Tests the case: two levels in the XML tree, same first level and leaves.
        Should return True.
        """
        requests_mock.get = self.get_mock

        self.assertTrue(compare('http://domain3.com/example3.xml', 'http://domain4.com/example4.xml'))

    @patch('sitemaps_compare.requests')
    def test_not_equal_different_leaves(self, requests_mock):
        """
        Tests the case: two levels in the XML tree, same first level but different leaves.
        Should return False.
        """

        def get_mock(url):
            """
            We must use a different mock for this one, to return different XML
            contents, given the same XML file (for different servers).
            """
            mock = Mock()
            if 'domain3.com/example2.xml' in url:
                mock.content = open('xmls/example2.xml', 'r').read()
            elif 'domain4.com/example2.xml' in url:
                mock.content = open('xmls/example5.xml', 'r').read()
            else:
                mock.content = open(
                        'xmls/{url}'.format(url=url[len('http://domainN.com/'):]), 
                        'r'
                    ).read()
            return mock

        requests_mock.get = get_mock

        self.assertFalse(compare('http://domain3.com/example3.xml', 'http://domain4.com/example4.xml'))
