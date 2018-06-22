import unittest
import glob
from spiders.cis_spider import Spider
from fake_response_from_file import fake_response_from_file


class TestCis(unittest.TestCase):
    maxDiff = None

    expected_parse = []
    expected_parse_cis = {'america-needs-federal-robotics-agency': False,
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
        self.spider = Spider()
        self.spider.print_only = True
        self.spider.testing = True
        self.expected_parse = glob.glob('test_pages/cis/parse/*.html')
        self.expected_parse = [page.split('/')[-1].split('\\')[-1].split('.')[0] for page in self.expected_parse]

    def test_parse(self):
        result = []
        for res in self.spider.parse(fake_response_from_file(url=self.url, path='test_pages/cis/')):
            result.append(self.url_to_filename(res.url))
            self.parse_urls.append(res.url)

        result = sorted(result)
        self.expected_parse = sorted(self.expected_parse)
        self.assertEqual(self.expected_parse, result)

    def test_parse_cis(self):
        result_dict = {}
        urls = [u for u in self.parse_urls if 'white-papers' not in u]
        for url in urls:
            res = self.spider.parse_cis(fake_response_from_file(url=url, path='test_pages/cis/parse/'))
            result_dict[self.url_to_filename(url)] = res

        for url in result_dict.keys():
            self.assertEqual(result_dict[url], self.expected_parse_cis[url],  'Expected ' + ('' if self.expected_parse_cis[url] else 'no ') + 'PDF in page ' + url)

    def url_to_filename(self, url):
        exploded_url = url.replace('?', '_').split('/')
        return exploded_url[-1] if exploded_url[-1] else exploded_url[-2]


if __name__ == '__main__':
    unittest.main()
