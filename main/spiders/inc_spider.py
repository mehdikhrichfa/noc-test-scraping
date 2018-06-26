import scrapy
try:
    from utils import print_url
except ImportError:
    from main.utils import print_url


class Spider(scrapy.Spider):
    name = 'inc'

    # Command line arguments
    print_only = False
    testing = False

    errors = 0
    retrieved = 0

    # URLs to scrape, automatically called by the Spider object
    start_urls = ['http://networkcultures.org/publications/']

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
        papers_css = '.pub-title a'
        next_css = 'a[title="Go to next page"]'
        parser = self.parse_inc

        papers = response.css(papers_css)

        # Crawl through each paper's page to retrieve the .pdf file
        for paper in papers:
            yield response.follow(paper, parser)

        # Go to the next page
        a = response.css(next_css)
        for x in a:  # Go to the next page to do the same thing again
            yield response.follow(x, callback=self.parse)

    def parse_inc(self, response):
        """"
        Takes the page dedicated to a single publication on the INC website, gets the pdf URL (if present on the page)
        and calls the function print_url

        :param response: Response object containing the INC page dedicated to a single publication
        """
        pdf_css = 'a[href$=".pdf"]::attr(href)'
        pdf_file = response.css(pdf_css).extract_first()  # Parse paper page

        if not pdf_file:
            pdf_css = '.pwk-link::attr(href)'
            pdf_file = response.css(pdf_css).extract_first()  # Parse paper page

        if not self.testing:
            print_url(self, response, pdf_file, self.name.upper())

            if (not self.print_only) and (pdf_file is not None):
                return {"file_urls": [response.urljoin(pdf_file)]}
        return False if pdf_file is None else True

    def closed(self, reason):
        """
        Called automatically before the end of the execution of the spider.
        Prints the number of files it found and the number of missing files (when the spider expected to find one).

        :param reason: String object containing the reason why the spider was closed
        """
        print('{} missing files: {}'.format(self.name.upper(), self.errors))
        print('{} retrieved files: {}'.format(self.name.upper(), self.retrieved))
