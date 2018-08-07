# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline
import scrapy
import json


class PDFPipeline(FilesPipeline):
    """
    Pipeline that processes pdf files download requests.
    """

    path_urls = dict()
    url_names = dict()

    def file_path(self, request, response=None, info=None):
        """
        Changes the filename of the pdf file to download to its default name (from the sha name given by Scrapy)
        :param request:
        :param response:
        :param info:
        :return: String object with the new filename
        """
        filename = request.url.split('/')[-1].replace('%20', ' ')
        question_mark = filename.rfind('?')
        if not question_mark == -1:
            filename = filename[:question_mark]

        self.path_urls[filename] = request.url
        return str(filename)

    def get_media_requests(self, item, info):
        """
        Associates, in a dictionary, URLs and titles of the files
        :param item: Item object containing the URL the file will be downloaded from and the title of the file
        :param info:
        :return: Request object containing the file URL
        """

        self.url_names[item['file_urls'][0]] = item['title'][:item['title'].rfind('|')].strip()
        yield scrapy.Request(item['file_urls'][0])

    def close_spider(self, spider):
        """
        Called when the spider is closed.
        Writes 2 JSON files:
            -   The first one associates file paths and file urls
            -   The second one associates file urls and file titles
        :param spider: Spider object that refers to the spider that was just closed
        """
        # Write paths and urls
        with open('path_urls.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.path_urls, indent=4))

        # Write names and urls
        with open('url_names.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.url_names, indent=4))
