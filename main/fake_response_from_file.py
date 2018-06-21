import os
from scrapy.http import TextResponse, Request


def fake_response_from_file(url=None, path=''):

    if not url:
        url = 'http://www.example.com'
    request = Request(url=url)

    path += [word for word in url.replace('?', '_').split('/') if word][-1] + '.html'  # last non empty element
    with open(path, 'r', encoding='utf-8') as file:
        file_content = file.read()
        response = TextResponse(url=url, request=request, body=file_content, encoding='utf-8')
        return response
