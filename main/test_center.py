import unittest
from scrapy.spider import Spider
from fake_response_from_file import fake_response_from_file


class TestCenter(unittest.TestCase):
    maxDiff = None

    expected_parse = []
    expected_parse_center = {}

    url = 'www.example.com'
    parse_urls = []

    def setUp(self, spider, expected_parse):
        self.spider = spider
        self.spider.print_only = True
        self.spider.testing = True
        self.expected_parse = [self.path_to_filename(page) for page in expected_parse]

    def path_to_filename(self, path):
        return path.split('/')[-1].split('\\')[-1].split('.')[0]

    def url_to_filename(self, url):
        exploded_url = url.replace('?', '_').split('/')
        return exploded_url[-1] if exploded_url[-1] else exploded_url[-2]


if __name__ == '__main__':
    unittest.main()
