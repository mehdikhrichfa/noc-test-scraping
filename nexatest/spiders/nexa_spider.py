import scrapy
from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser
from colorama import init, Fore, Style
init()


class NexaSpider(scrapy.Spider):
    name = 'nexa'

    errors = {
        'BKC': 0,
        'NEXA': 0,
        'CIS': 0,
        'INC': 0,
        'YALE': 0,
    }

    retrieved = {
        'BKC': 0,
        'NEXA': 0,
        'CIS': 0,
        'INC': 0,
        'YALE': 0,
    }

    start_urls = [                                           # URLs to scrape, automatically called by the Spider object
        'https://nexa.polito.it/papers',
        'https://cyber.harvard.edu/publications',
        'http://cyberlaw.stanford.edu/publications/white-papers',
        'http://networkcultures.org/publications/',
        'https://law.yale.edu/isp/publications',
    ]

    def parse(self, response):
        """
        Takes all the URLs in the publication page and parses the content of the
        web page by its css selectors

        :param response: Response object containing the 'publications' web page
        :return: Request object containing the next page to scrape
        """
        sources = (                                                              # Currently somewhat supported websites
                ('nexa', 'ul:not(.menu):not(.pager) a', self.parse_NEXA),
                ('harvard', '.node-readmore a', self.parse_BKC),
                ('stanford', 'header:not([role="banner"]) a', self.parse_CIS),
                ('networkcultures', '.pub-title a', self.parse_INC),
                ('yale', 'stay', self.parse_YALE)
            )

        for center, css, parser in sources:                            # Select the most appropriate parser for the task
            if center in response.url:
                papers = response.css(css) if css != 'stay' else [response.url]
                parse_paper = parser
                break
        
        for paper in papers:                                 # Crawl through each paper's page to retrieve the .pdf file
            yield response.follow(paper, parse_paper)
        
        if response.css('a[title="Go to next page"]'):                  # Go to the next page to do the same thing again
            a = response.css('a[title="Go to next page"]')[0]
            yield response.follow(a, callback=self.parse)
        elif response.css('.next a'):
            a = response.css('.next a')[0]
            yield response.follow(a, callback=self.parse, dont_filter=True)

    def parse_BKC(self, response):                                               # Parse a BKC paper page
        """
        Takes the page dedicated to a single publication on the BKC website and either continues crawling to a
        'publication repository' or downloads the pdf (if present on the page itself)

        :param response: Response object containing the BKC page dedicated to a single publication
        :return: Request object containing the 'publication repository' page dedicated to the current publication
        """
        links = response.css('.field-item a::attr(href)').extract()
        found = False
        if links is not None:
            for link in links:
                if 'ssrn' in link:
                    yield response.follow(link.replace('&download=yes', ''), self.parse_SSRN)
                    found = True
                    break
                elif 'dash' in link:
                    yield response.follow(link, self.parse_DASH)
                    found = True
                    break
                elif 'arxiv' in link:
                    yield response.follow(link, self.parse_ARXIV)
                    found = True
                    break
                elif '.pdf' in link:
                    self.print_url(response, link, 'BKC')
                    found = True
                    break
        if not found:
            self.print_url(response, None, 'BKC')

    def parse_SSRN(self, response):                                       # Parse the SSRN page to obtain the paper link
        """
        Takes the SSRN (Social Science Research Network) web page, gets the .pdf URL and calls the function print_url

        :param response: Response object containing the SSRN (Social Science Research Network) page dedicated to the BKC
                         paper
        """
        pdf_file = response.css('.download-button::attr(href)').extract_first()
        self.print_url(response, pdf_file, 'BKC')

    def parse_DASH(self, response):                                       # Parse the DASH page to obtain the paper link
        """
        Takes the DASH (Digital Access to Scholarship at Harvard) web page, gets the .pdf URL and calls the
        print_url function

        :param response: Response object containing the DASH (Digital Access to Scholarship at Harvard) page dedicated
        to the BKC paper
        """
        pdf_file = response.css('.dash-item-download a::attr(href)').extract_first()
        self.print_url(response, pdf_file, 'BKC')

    def parse_ARXIV(self, response):
        """
        Takes the ArXiv web page, gets the .pdf URL and calls the function print_url

        :param response: Response object containing the ArXiv page dedicated to the BKC paper
        """
        pdf_file = response.css('.full-text a::attr(href)').extract_first()
        self.print_url(response, pdf_file, 'BKC')

    def parse_NEXA(self, response):                                             # Parse a NEXA Center paper page
        """
        Takes the page dedicated to a single publication on the Nexa website, gets the pdf URL (if present on the page)
        and calls the function print_url

        :param response: Response object containing the Nexa page dedicated to a single publication
        """
        pdf_file = response.css('.file a::attr(href)').extract_first()
        if not pdf_file:
            pdf_file = response.css('.field-item a[href$=".pdf"]::attr(href)').extract_first()
        self.print_url(response, pdf_file, 'NEXA')

    def parse_CIS(self, response):
        """"
        Takes the page dedicated to a single publication on the CIS website, gets the pdf URL (if present on the page)
        and calls the function print_url

        :param response: Response object containing the CIS page dedicated to a single publication
        """
        pdf_file = response.css('.file a::attr(href)').extract_first()          # Parse CIS paper page
        if not pdf_file:
            pdf_file = response.css('.field-item a[href$=".pdf"]::attr(href)').extract_first()
        self.print_url(response, pdf_file, 'CIS')

    def parse_INC(self, response):
        """"
        Takes the page dedicated to a single publication on the INC website, gets the pdf URL (if present on the page)
        and calls the function print_url

        :param response: Response object containing the INC page dedicated to a single publication
        """
        pdf_file = response.css('a[href$=".pdf"]::attr(href)').extract_first()
        self.print_url(response, pdf_file, 'INC')

    def parse_YALE(self, response):
        """
        Takes the whole publications page, scrapes the papers on it one by one and, for each one, calls the function
        print_url.
        The YALE ISP website does not have dedicated pages for single publications.

        :param response: Response object containing the YALE publications page
        """
        pdf_files = response.css('a[href$=".pdf"]::attr(href)').extract()
        for pdf_file in pdf_files:
            self.print_url(response, pdf_file, 'YALE')

    def print_url(self, response, pdf_file, center):
        """
        Prints the URL of pdf_file or the url of the last web page reached before giving up on a particular publication
        and counts the number of successes and failures in retrieving the publications.

        :param response: Response object containing the last website reached before finding the pdf file or giving up
        :param pdf_file: String object containing the URL of the paper in pdf format. It is None if the pdf was not
                        found
        :param center: String object containing the name of the center whose website the spider is currently crawling
        """
        if pdf_file is not None:
            color = Fore.GREEN
            text = pdf_file
            self.retrieved[center] += 1

        else:
            color = Fore.RED
            text = 'No pdf file found in ' + response.url
            self.errors[center] += 1

        print(Style.BRIGHT + color + '--------------------------------------------------------------')
        print('[' + center + '] - ' + text)
        print('--------------------------------------------------------------' + Style.RESET_ALL)

    def closed(self, reason):
        """
        Called automatically before the end of the execution of the spider.
        Prints the number of files it found and the number of missing files (when the spider expected to find one).


        :param reason: String object containing the reason why the spider was closed
        """
        for center, num_errors in self.errors.items():
            print('{} missing files: {}'.format(center, str(num_errors)))
        for center, num_files in self.retrieved.items():
            print('{} retrieved files: {}'.format(center, str(num_files)))
