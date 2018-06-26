import unittest
from spiders.isp_spider import Spider
from fake_response_from_file import fake_response_from_file
import test_center


class TestIsp(test_center.TestCenter):

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
        spider = Spider()
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


if __name__ == '__main__':
    unittest.main()
