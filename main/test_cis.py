import unittest
import glob
from spiders.cis_spider import Spider
from fake_response_from_file import fake_response_from_file


class TestCis(unittest.TestCase):
    maxDiff = None

    expected_parse = []
    expected_parse_cis = [False, True, True, True, True, True, True, True, False, True]

    url = 'http://cyberlaw.stanford.edu/publications/white-papers'
    parse_urls = []

    def setUp(self):
        self.spider = Spider()
        self.spider.print_only = True
        self.spider.testing = True
        self.expected_parse = glob.glob('test_pages/cis/parse/*.html')
        self.expected_parse = [page.split('/')[-1].split('\\')[-1].split('.')[0] for page in self.expected_parse]

    def test_parse(self):
        result = []
        for res in self.spider.parse(fake_response_from_file(url=self.url, path='test_pages/cis/')):
            result.append([word for word in res.url.replace('?', '_').split('/') if word][-1])
            self.parse_urls.append(res.url)

        self.assertEqual(sorted(result), sorted(self.expected_parse))

    def test_parse_cis(self):
        result = []
        for url in [u for u in self.parse_urls if 'white-papers' not in u]:
            res = self.spider.parse_cis(fake_response_from_file(url=url, path='test_pages/cis/parse/'))
            result.append(res)
        self.assertEqual(sorted(result), sorted(self.expected_parse_cis))


if __name__ == '__main__':
    unittest.main()
