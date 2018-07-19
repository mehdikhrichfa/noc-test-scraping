import scrapy
try:
    from utils import print_url
except ImportError:
    from main.utils import print_url


class Spider(scrapy.Spider):
    name = 'bkc'

    # Command line arguments
    print_only = False
    testing = False

    errors = 0
    retrieved = 0

    # URLs to scrape, automatically called by the Spider object
    start_urls = ['https://cyber.harvard.edu/publications']

    file_urls = []

    def __init__(self, **kwargs):
        """
        Takes a command line argument and runs it

        :param args: String object containing the command line arguments
        """
        if 'print_only' in kwargs:
            self.print_only = kwargs['print_only'].upper() == 'TRUE'

    def parse(self, response):
        """
        Takes all the URLs in the publication page and parses the content of the
        web page by its css selectors

        :param response: Response object containing the 'publications' web page
        :return: Request object containing the next page to scrape
        """
        papers_css = '.c-unique-item a'
        next_css = 'a[title="Go to next page"]'
        parser = self.parse_bkc

        papers = response.css(papers_css)

        # Crawl through each paper's page to retrieve the .pdf file
        for paper in papers:
            yield response.follow(paper, parser)

        # Go to the next page
        a = response.css(next_css)
        for x in a:  # Go to the next page to do the same thing again
            yield response.follow(x, callback=self.parse)

    def parse_bkc(self, response):                                               # Parse a BKC paper page
        """
        Takes the page dedicated to a single publication on the BKC website and either continues crawling to a
        'publication repository' or downloads the pdf (if present on the page itself)

        :param response: Response object containing the BKC page dedicated to a single publication
        :return: Request object containing the 'publication repository' page dedicated to the current publication
        """
        website_css = '.c-detail__nav a::attr(href)'
        links = response.css(website_css).extract()
        found = False
        parser = None
        if links is not None:
            for link in links:
                if 'ssrn' in link:
                    parser = self.parse_SSRN
                    found = True
                    break
                elif 'dash' in link:
                    parser = self.parse_DASH
                    found = True
                    break
                elif 'arxiv' in link:
                    parser = self.parse_ARXIV
                    found = True
                    break
                elif '.pdf' in link:
                    found = True
                    break
        if self.testing:
            return found

        if found:
            if parser is not None:
                return response.follow(link.replace('&download=yes', ''), parser)
            else:
                print_url(self, response, link, self.name.upper())
                if not self.print_only:
                    return {"file_urls": [response.urljoin(link)]}
        else:
            print_url(self, response, None, self.name.upper())

    def parse_SSRN(self, response):                                       # Parse the SSRN page to obtain the paper link
        """
        Takes the SSRN (Social Science Research Network) web page, gets the .pdf URL and calls the function print_url

        :param response: Response object containing the SSRN (Social Science Research Network) page dedicated to the BKC
                         paper
        """
        pdf_css = '.download-button::attr(href)'
        pdf_file = response.css(pdf_css).extract_first()
        print_url(self, response, pdf_file, self.name.upper())
        if (not self.print_only) and (pdf_file is not None):
            return {"file_urls": [response.urljoin(pdf_file) + '&download=yes']}

    def parse_DASH(self, response):                                       # Parse the DASH page to obtain the paper link
        """
        Takes the DASH (Digital Access to Scholarship at Harvard) web page, gets the .pdf URL and calls the
        print_url function

        :param response: Response object containing the DASH (Digital Access to Scholarship at Harvard) page dedicated
        to the BKC paper
        """
        pdf_css = '.dash-item-download a::attr(href)'
        pdf_file = response.css(pdf_css).extract_first()
        print_url(self, response, pdf_file, self.name.upper())
        if (not self.print_only) and (pdf_file is not None):
            return {"file_urls": [response.urljoin(pdf_file)]}

    def parse_ARXIV(self, response):
        """
        Takes the ArXiv web page, gets the .pdf URL and calls the function print_url

        :param response: Response object containing the ArXiv page dedicated to the BKC paper
        """
        pdf_css = '.full-text a::attr(href)'
        pdf_file = response.css(pdf_css).extract_first()
        print_url(self, response, pdf_file, self.name.upper())
        if (not self.print_only) and (pdf_file is not None):
            return {"file_urls": [response.urljoin(pdf_file)]}

    def closed(self, reason):
        """
        Called automatically before the end of the execution of the spider.
        Prints the number of files it found and the number of missing files (when the spider expected to find one).

        :param reason: String object containing the reason why the spider was closed
        """
        print('{} missing files: {}'.format(self.name.upper(), self.errors))
        print('{} retrieved files: {}'.format(self.name.upper(), self.retrieved))
