import unittest
import glob
from spiders.cis_spider import Spider
from fake_response_from_file import fake_response_from_file
import test_center


class TestCis(test_center.TestCenter):

    expected_parse_center = {'america-needs-federal-robotics-agency': False,
                             'slowing-down-presses-relationship-between-net-neutrality-and-local-news': True,
                             'comments-mozillas-proposal': True,
                             'automated-and-autonomous-driving-regulation-under-uncertainty': True,
                             'network-neutrality-and-zero-rating': True,
                             'open-access-publishing-literature-review': True,
                             'proceedings-volume': True,
                             'risks-responsible-encryption': True,
                             'cybersecurity-states-lessons-across-america': False,
                             'sesta-and-teachings-intermediary-liability': True}

    url = 'http://cyberlaw.stanford.edu/publications/white-papers'
    parse_urls = []

    def setUp(self):
        spider = Spider()
        expected_parse = glob.glob('test_pages/cis/parse/*.html')
        super().setUp(spider, expected_parse)

    def test_parse(self):
        result = []
        for res in self.spider.parse(fake_response_from_file(url=self.url, path='test_pages/cis/')):
            result.append(self.url_to_filename(res.url))
            self.parse_urls.append(res.url)

        result = sorted(result)
        self.expected_parse = sorted(self.expected_parse)

        for page in [x for x in self.expected_parse if x in self.expected_parse and x not in result]:
            raise AssertionError('Page ' + page + ' not found!')
        for page in [x for x in result if x in result and x not in self.expected_parse]:
            raise AssertionError('Page ' + page + ' was not supposed to be scraped.')

    def test_parse_cis(self):
        result_dict = {}
        urls = [u for u in self.parse_urls if 'white-papers' not in u]
        for url in urls:
            res = self.spider.parse_cis(fake_response_from_file(url=url, path='test_pages/cis/parse/'))
            result_dict[self.url_to_filename(url)] = res

        for url in result_dict.keys():
            self.assertEqual(result_dict[url], self.expected_parse_center[url],
                             'Expected ' + ('' if self.expected_parse_center[url] else 'no ') + 'PDF in page ' + url)


if __name__ == '__main__':
    unittest.main()
