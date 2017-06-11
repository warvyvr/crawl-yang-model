# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import datetime

class YangModelPipeline(object):
    items = []
    start_time = None

    def open_spider(self, spider):
        self.file = open("r.json","w")
        self.start_time = str(datetime.datetime.today())

    def close_spider(self, spider):
        result = {}

        for i in self.items:
            area = i['area']
            wg = i['wg']
            obj = {"name": i['title'], 'url':i['url'],"models":i['yangs'],"category":i['category']}
            if result.has_key(area):
                if result[area].has_key(wg):
                    result[area][wg].append(obj)
                else:
                    result[area][wg] = [obj]
            else:
                result[area] = {wg:[obj]}

        result['meta'] = {
            'bad_requests' : spider.bad_urls,
            'start_time' : str(self.start_time),
            'finish_time': str(datetime.datetime.today()),
        }

        line = json.dumps(result, indent=4, separators=(',', ': ')) + "\n"
        self.file.write(line)
        self.file.close()


    def process_item(self, item, spider):
        #line = json.dumps(dict(item)) + ",\n"
        #self.file.write(line)
        #return item
        self.items.append(item)
