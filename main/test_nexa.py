import unittest
import glob
from spiders.nexa_spider import Spider
from fake_response_from_file import fake_response_from_file
import test_center


class TestNexa(test_center.TestCenter):

    expected_parse_center = {'1351': True,
                             '1354': True,
                             '1467': True,
                             '1468': True,
                             '1469': True,
                             '1470': True,
                             '1471': True,
                             '2017-annual-report': True,
                             'futia2017Contratti': False,
                             'futia2017ContrattiPubblici': False}

    url = 'https://nexa.polito.it/papers'
    parse_urls = []

    def setUp(self):
        spider = Spider()
        expected_parse = glob.glob('test_pages/nexa/parse/*.html')
        super().setUp(spider, expected_parse)

    def test_parse(self):
        result = []
        for res in self.spider.parse(fake_response_from_file(url=self.url, path='test_pages/nexa/')):
            result.append(self.url_to_filename(res.url))
            self.parse_urls.append(res.url)

        result = sorted(result)
        self.expected_parse = sorted(self.expected_parse)

        for page in [x for x in self.expected_parse if x in self.expected_parse and x not in result]:
            raise AssertionError('Page ' + page + ' not found!')
        for page in [x for x in result if x in result and x not in self.expected_parse]:
            raise AssertionError('Page ' + page + ' was not supposed to be scraped.')

    def test_parse_nexa(self):
        result_dict = {}
        urls = [u for u in self.parse_urls if 'page=' not in u]
        for url in urls:
            res = self.spider.parse_nexa(fake_response_from_file(url=url, path='test_pages/nexa/parse/'))
            result_dict[self.url_to_filename(url)] = res

        for url in result_dict.keys():
            self.assertEqual(result_dict[url], self.expected_parse_center[url],
                             'Expected ' + ('' if self.expected_parse_center[url] else 'no ') + 'PDF in page ' + url)


if __name__ == '__main__':
    unittest.main()
