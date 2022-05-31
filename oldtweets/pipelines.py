# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy import signals
from scrapy.exporters import CsvItemExporter
import csv


class OldtweetsPipeline:
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        f = open(f'{spider.name}_items.csv', 'w+b')
        self.files[spider] = f
        self.exporter = CsvItemExporter(f)
        self.exporter.fields_to_export = ['title', 'handle', 'text', 'deleted']
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        f = self.files.pop(spider)
        f.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
