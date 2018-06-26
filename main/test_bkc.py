import unittest
import glob
from spiders.bkc_spider import Spider
from fake_response_from_file import fake_response_from_file
import test_center


class TestBKC(test_center.TestCenter):

    expected_parse_center = {'100108': True,
                             '100137': False,
                             '100163': True,
                             '100169': False,
                             '100181': True,
                             'AIExplanation': True,
                             'berklett': True,
                             'BigDataPrivacy': True,
                             'biomedicalelite': True,
                             'Chattanooga': True,
                             'communityfiber': True,
                             'Concord': True,
                             'DefiningHateSpeech': True,
                             'fibercompetition': True,
                             'GlobalInternetCensorship': True,
                             'GrassrootsPerspectives': True,
                             'harmfulspeech': True,
                             'HateSpeechIndia': True,
                             'mediacloud': True,
                             'OpenDataBriefing': True,
                             'opendataprivacyplaybook': True,
                             'openletter': True,
                             'OrganizationStructure': True,
                             'PolicyPositionsonSOPA-PIPA': True,
                             'StudentPrivacyBriefing': True,
                             'transparency_guide_and_template': True,
                             'UnderstandingHarmfulSpeech': True,
                             'WikipediaCensorship': True,
                             'yemen': True,
                             'zerorating': True}

    url = 'https://cyber.harvard.edu/publications'
    parse_urls = []

    def setUp(self):
        spider = Spider()
        expected_parse = glob.glob('test_pages/bkc/parse/*.html')
        super().setUp(spider, expected_parse)

    def test_parse(self):
        result = []
        for res in self.spider.parse(fake_response_from_file(url=self.url, path='test_pages/bkc/')):
            result.append(self.url_to_filename(res.url))
            self.parse_urls.append(res.url)

        result = sorted(result)
        self.expected_parse = sorted(self.expected_parse)

        for page in [x for x in self.expected_parse if x in self.expected_parse and x not in result]:
            raise AssertionError('Page ' + page + ' not found!')
        for page in [x for x in result if x in result and x not in self.expected_parse]:
            raise AssertionError('Page ' + page + ' was not supposed to be scraped.')

    def test_parse_bkc(self):
        result_dict = {}
        urls = [u for u in self.parse_urls if 'page=' not in u]

        if not urls:
            raise AssertionError('No URLs retrieved!')

        for url in urls:
            res = self.spider.parse_bkc(fake_response_from_file(url=url, path='test_pages/bkc/parse/'))
            result_dict[self.url_to_filename(url)] = res

        for url in result_dict.keys():
            self.assertEqual(result_dict[url], self.expected_parse_center[url],
                             'Expected ' + ('' if self.expected_parse_center[url] else 'no ') + 'PDF in page ' + url)


if __name__ == '__main__':
    unittest.main()
