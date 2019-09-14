# -*- coding: utf-8 -*-
import scrapy
from spider_doutula.items import SpiderDoutulaItem
from spider_doutula.settings import ALL_PAGE_NUM

item = SpiderDoutulaItem()


class DoutuSpider(scrapy.Spider):
    name = 'doutu'
    allowed_domains = ['https://www.doutula.com']
    head_url = 'https://www.doutula.com/photo/list/?page='
    start_urls = [f'{head_url}1']

    def make_requests_from_url(self, url):
        return scrapy.Request(url=url, meta={"download_timeout": 10}, callback=self.parse)

    def parse(self, response):
        # 详情页面url_list
        details_url_list = response.selector.xpath(
            "//div[@class='page-content text-center']/div/a/@href").extract()
        for url in details_url_list:
            yield scrapy.Request(url, callback=self.detail_parse, dont_filter=True)
        current_page_num = int((response.url).split('=')[1])
        if current_page_num < ALL_PAGE_NUM:
            next_url = self.head_url + str(current_page_num + 1)
            yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)

    def detail_parse(self, response):
        item = SpiderDoutulaItem()
        tags = response.selector.xpath("//div[@class='pic-tips']/a/text()").extract()
        pic_url = response.selector.xpath("//div[@class='swiper-slide']/div/table/tbody/tr/td/img/@src").extract()
        item['pic_url'] = pic_url[0]
        item['tags'] = tags
        yield item
