# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

collection = pymongo.MongoClient('127.0.0.1',27017)
db = collection.cool

class SaveMongoPipeline(object):
    def process_item(self, item, spider):
    	db.mafengwo.update({'uid':item['uid']}, {'$set':dict(item)},upsert=True)
        return item
