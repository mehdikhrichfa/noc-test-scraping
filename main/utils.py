from colorama import init, Fore, Style
init()


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
        self.retrieved += 1
    else:
        color = Fore.RED
        text = 'No pdf file found in ' + response.url
        self.errors += 1

    print(Style.BRIGHT + color + '--------------------------------------------------------------')
    print('[' + center + '] - ' + text)
    print('--------------------------------------------------------------' + Style.RESET_ALL)
