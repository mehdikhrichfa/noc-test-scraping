# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline
import scrapy
import json


class Pipeline(object):

    def process_item(self, item, spider):
        return item


class PDFPipeline(FilesPipeline):
    # count_404 = 0
    # broken = dict()

    # @classmethod
    # def from_crawler(cls, crawler):
    #     settings = crawler.settings
    #     print("\n\nHERE\n\n")
    #     basepath = settings.get('FILES_STORE')
    #     return cls(basepath=basepath)
    #
    # def __init__(self, basepath):
    #     print("\n\n\n\n\n\n\n\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n\n\n\n\n\n\n")
    #     self.basepath = basepath

    path_urls = dict()

    def file_path(self, request, response=None, info=None):
        # print(request.url)
        # print(self.basepath)
        filename = request.url.split('/')[-1].replace('%20', ' ')
        question_mark = filename.rfind('?')
        if not question_mark == -1:
            # print("Question mark!!!")
            filename = filename[:question_mark]

        self.path_urls[filename] = request.url

        return str(filename)

    def get_media_requests(self, item, info):
        yield scrapy.Request(item['file_urls'][0])

    def close_spider(self, spider):
        # Write paths and urls
        with open('path_urls.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.path_urls, indent=4))

        # with open('broken.json', 'w', encoding='utf-8') as broken_pdfs:
        #     broken_pdfs.write(json.dumps(self.broken, indent=4))

    # def item_completed(self, results, item, info):
    #     if not results[0][0]:
    #         self.broken[item['url']] = item['file_urls'][0]
