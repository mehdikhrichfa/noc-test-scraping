import unittest
import glob
from spiders.inc_spider import Spider
from fake_response_from_file import fake_response_from_file
import test_center


class TestInc(test_center.TestCenter):

    expected_parse_center = {'tod-27-videoblogging-before-youtube': True,
                             'culture-of-the-selfie': True,
                             'deep-pockets-2-shadowbook-writing-through-the-digital-2014-2018': True,
                             'general-theory-of-the-precariat': True,
                             'moneylab-reader-2-overcoming-the-hype': True,
                             'organization-after-social-media': False,
                             'the-riddle-of-the-real-city-or-the-dark-knowledge-of-urbanism': False,
                             'tod-26-on-editorialization-structuring-space-and-authority-in-the-digital-age': True,
                             'zero-infinite-3-listing-technology': False,
                             'zero-infinite-4-the-online-self': False}

    url = 'http://networkcultures.org/publications/'
    parse_urls = []

    def setUp(self):
        spider = Spider()
        expected_parse = glob.glob('test_pages/inc/parse/*.html')
        super().setUp(spider, expected_parse)

    def test_parse(self):
        result = []
        for res in self.spider.parse(fake_response_from_file(url=self.url, path='test_pages/inc/')):
            result.append(self.url_to_filename(res.url))
            self.parse_urls.append(res.url)

        result = sorted(result[0:10])
        self.expected_parse = sorted(self.expected_parse)

        for page in [x for x in self.expected_parse if x in self.expected_parse and x not in result]:
            raise AssertionError('Page ' + page + ' not found!')
        for page in [x for x in result if x in result and x not in self.expected_parse]:
            raise AssertionError('Page ' + page + ' was not supposed to be scraped.')

    def test_parse_inc(self):
        result_dict = {}
        urls = self.parse_urls[0:10]

        if not urls:
            raise AssertionError('No URLs retrieved!')

        for url in urls:
            res = self.spider.parse_inc(fake_response_from_file(url=url, path='test_pages/inc/parse/'))
            result_dict[self.url_to_filename(url)] = res

        for url in result_dict.keys():
            self.assertEqual(result_dict[url], self.expected_parse_center[url],
                             'Expected ' + ('' if self.expected_parse_center[url] else 'no ') + 'PDF in page ' + url)


if __name__ == '__main__':
    unittest.main()
