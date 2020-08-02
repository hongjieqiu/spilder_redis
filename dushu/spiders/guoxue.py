import uuid
from scrapy_redis.spiders import RedisSpider
from scrapy.http import  Request

from dushu.items import DushuItem


class GuoxueSpider(RedisSpider):
    name = 'guoxue'
    allowed_domains = ['dushu.com']
    #爬虫开始的地址  可以随便写
    redis_key = 'gx_starl_urls'

    def parse(self, response):
        for url in response.css('.sub-catalog a::attr("href")').extract():
            yield Request('http://www.dushu.com' + url, callback=self.parse_item)
    def parse_item(self,response):
        divs = response.css('.book-info')
        for div in divs:
            item = DushuItem()
            item['id'] = uuid.uuid4().hex
            item['name'] = div.xpath('./div//img/@alt').get()
            item['cover'] = div.xpath('./div//img/@scr').get()
            item['detail_url'] = div.xpath('./div/a/@href').get()
            yield item
        #下一页
        next_url = response.css('.pages').xpath('./a[last()]/@href').get()
        yield Request('http://www.dushu.com' + next_url, callback=self.parse_item)