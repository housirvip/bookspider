# -*- coding: utf-8 -*-
from scrapy import Selector, Spider, Request
from scrapy.http import Response

from bookspider.items import EssayItem


class BiQiuGeSpider(Spider):
    name = 'biqiuge'
    allowed_domains = ['www.biqiuge.com']
    start_urls = ['https://www.biqiuge.com/book/16513/']

    def parse(self, response: Response):
        a_list = response.xpath("//div[@class='listmain']/dl/dd/a")
        for a in a_list:
            uri = a.xpath("@href").get()
            url = response.urljoin(uri)
            yield Request(url, callback=self.parse_essay)

    def parse_essay(self, response: Selector):
        div = response.xpath("//div[@class='content']")
        title = div.xpath("h1/text()").get()
        content_list = div.xpath("div[@id='content']/text()").getall()
        content = ''.join(content_list).strip()
        self.logger.info(title)
        return EssayItem(title=title, content=content)
