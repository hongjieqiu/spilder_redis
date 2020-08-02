# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from dushu.db import BaseDao
from dushu.items import DushuItem


class DushuPipeline:
    def __init__(self):
        self.dao = BaseDao()
        self.table = 'dushu_table'
    def process_item(self, item, spider):
        print('-------------------', item)
        if isinstance(item, DushuItem):
            item['spilderName'] = spider.name
            self.dao.save(self.table, **item)
            spider.logger.info(f"{item} 成功写入sql")
        return item
