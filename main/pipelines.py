# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline
import scrapy
import main.settings
import os


class Pipeline(object):

    def process_item(self, item, spider):
        return item


class PDFPipeline(FilesPipeline):
    # count_404 = 0

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

    def file_path(self, request, response=None, info=None):
        # print(request.url)
        # print(self.basepath)
        filename = request.url.split('/')[-1].replace('%20', ' ')
        question_mark = filename.rfind('?')
        if not question_mark == -1:
            # print("Question mark!!!")
            filename = filename[:question_mark]
        # with open("full/" + os.path.splitext(filename)[0] + ".txt") as url_file:
        #     url_file.write(request.url)
        #

        return "pdf/{}".format(str(filename))

    def get_media_requests(self, item, info):
        yield scrapy.Request(item['file_urls'][0])

    # def item_completed(self, results, item, info):
    #     if not results[0][0]:
    #         self.count_404 += 1
    #     print(self.count_404)
