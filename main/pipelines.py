# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline


class Pipeline(object):
    def process_item(self, item, spider):
        return item


class PDFPipeline(FilesPipeline):

    filename = 0

    def file_path(self, request, response=None, info=None):

        PDFPipeline.filename += 1
        print(str(PDFPipeline.filename) + "\n\n\n\n\n")
        return "full/{}.pdf".format(str(self.filename))

    def get_media_request(self, item, info):
        print('\n\n\n' + str(info) + '\n\n\n')
        for file_url in item["file_urls"]:
            yield scrapy.Request(file_url)
