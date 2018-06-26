import unittest
import glob
from fake_response_from_file import fake_response_from_file
from spiders.nexa_spider import Spider as SpiderNexa
from spiders.isp_spider import Spider as SpiderIsp
from spiders.cis_spider import Spider as SpiderCis
from spiders.inc_spider import Spider as SpiderInc
from spiders.bkc_spider import Spider as SpiderBkc


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




class TestBKC(TestCenter):

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
        spider = SpiderBkc()
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



class TestCis(TestCenter):

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
        spider = SpiderCis()
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

        if not urls:
            raise AssertionError('No URLs retrieved!')

        for url in urls:
            res = self.spider.parse_cis(fake_response_from_file(url=url, path='test_pages/cis/parse/'))
            result_dict[self.url_to_filename(url)] = res

        for url in result_dict.keys():
            self.assertEqual(result_dict[url], self.expected_parse_center[url],
                             'Expected ' + ('' if self.expected_parse_center[url] else 'no ') + 'PDF in page ' + url)


class TestInc(TestCenter):

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
        spider = SpiderInc()
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


class TestIsp(TestCenter):

    expected_parse_center = ['governing_machine_learning_-_final',
                             '21._amicus_brief',
                             'hacking_the_election_conference_report_11.01.16',
                             'yls_rop_report97097677_2',
                             'a2k_global-censorship_2',
                             'yale_isp_amicus_final',
                             '16-16067_under_seal_v._loretta_e._lynch_brief_of_amici_curiae_floyd_abrams_institute_for_freedom_of_expression_and_first_amendment_scholars_in_support_of_the_petition_for_rehearing_and_rehearing_en_banc8',
                             'beyond_intermediary_liability_-_workshop_report',
                             'yale_isp_and_scholars_of_ip_and_free_expression_amicus_brief',
                             'fighting_fake_news_-_workshop_report']

    url = 'https://law.yale.edu/isp/publications'
    parse_urls = []

    def setUp(self):
        spider = SpiderIsp()
        expected_parse = ['governing_machine_learning_-_final.pdf',
                          '21._amicus_brief.pdf',
                          'hacking_the_election_conference_report_11.01.16.pdf',
                          'yls_rop_report97097677_2.pdf',
                          'a2k_global-censorship_2.pdf',
                          'yale_isp_amicus_final.pdf',
                          '16-16067_under_seal_v._loretta_e._lynch_brief_of_amici_curiae_floyd_abrams_institute_for_freedom_of_expression_and_first_amendment_scholars_in_support_of_the_petition_for_rehearing_and_rehearing_en_banc8.pdf',
                          'beyond_intermediary_liability_-_workshop_report.pdf',
                          'yale_isp_and_scholars_of_ip_and_free_expression_amicus_brief.pdf',
                          'fighting_fake_news_-_workshop_report.pdf',
                          'publications_page=1.html']
        super().setUp(spider, expected_parse)

    def test_parse(self):
        result = []
        for res in self.spider.parse(fake_response_from_file(url=self.url, path='test_pages/isp/')):
            result.append(self.path_to_filename(self.url_to_filename(res.url)))
            self.parse_urls.append(res.url)

        result = sorted(result)
        self.expected_parse = sorted(self.expected_parse)

        for page in [x for x in self.expected_parse if x in self.expected_parse and x not in result]:
            raise AssertionError('Page ' + page + ' not found!')
        for page in [x for x in result if x in result and x not in self.expected_parse]:
            raise AssertionError('Page ' + page + ' was not supposed to be scraped.')

    def test_parse_isp(self):

        result = []
        for res in self.spider.parse_isp(fake_response_from_file(url=self.url, path='test_pages/isp/')):
            result.append(self.path_to_filename(self.url_to_filename(res.url)))
            self.parse_urls.append(res.url)

        result = sorted(result)
        self.expected_parse_center = sorted(self.expected_parse_center)

        for page in [x for x in self.expected_parse_center if x in self.expected_parse_center and x not in result]:
            raise AssertionError('Pdf ' + page + ' not found!')
        for page in [x for x in result if x in result and x not in self.expected_parse_center]:
            raise AssertionError('Pdf ' + page + ' was not supposed to be scraped.')


class TestNexa(TestCenter):

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
        spider = SpiderNexa()
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

        if not urls:
            raise AssertionError('No URLs retrieved!')

        for url in urls:
            res = self.spider.parse_nexa(fake_response_from_file(url=url, path='test_pages/nexa/parse/'))
            result_dict[self.url_to_filename(url)] = res

        for url in result_dict.keys():
            self.assertEqual(result_dict[url], self.expected_parse_center[url],
                             'Expected ' + ('' if self.expected_parse_center[url] else 'no ') + 'PDF in page ' + url)


if __name__ == '__main__':
    unittest.main()
