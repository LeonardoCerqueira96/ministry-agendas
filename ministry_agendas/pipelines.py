# Developed by: Leonardo Cesar Cerqueira

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

# This class is responsible for gathering all the yielded items from the parser
# into a list, sort it by the event date, then write it to a JSON file
class MinistryAgendasPipeline(object):
    def open_spider(self, spider):
        self.agenda_list = []
        return
    
    def process_item(self, item, spider):
        self.agenda_list.append(item)
        return item

    def close_spider(self, spider):
        self.agenda_list = sorted(self.agenda_list, key=lambda a: a["EventDate"])
        
        with open("agendas.json", "w") as f:
            json.dump(self.agenda_list, f, indent=4, default=str, ensure_ascii=False)

        return
