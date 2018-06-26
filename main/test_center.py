import unittest


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
        path = path.split('/')[-1].split('\\')[-1]
        return path[:path.rindex('.') if '.' in path else None]

    def url_to_filename(self, url):
        exploded_url = url.replace('?', '_').split('/')
        return exploded_url[-1] if exploded_url[-1] else exploded_url[-2]


if __name__ == '__main__':
    unittest.main()
