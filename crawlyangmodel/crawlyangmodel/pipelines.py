# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class YangModelPipeline(object):

    def open_spider(self, spider):
        self.file = open("tmp.json","wb")
        self.file.write("[\n")

    def close_spider(self, spider):
        self.file.write("{}]\n")
        self.file.close()
        self.file = None


    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + ",\n"
        self.file.write(line)
        return item
