# -*- coding: utf-8 -*-
import scrapy


class InvisibleBreadSpider(scrapy.Spider):
    name = 'invisible_bread'
    allowed_domains = [
            'feeds.feedburner.com/InvisibleBread',
            'invisiblebread.com']
    start_urls = ['http://feeds.feedburner.com/InvisibleBread/']

    def parse(self, response):
        for item in response.css('item'):
            info = {}
            info['title'] = item.css('title::text').extract_first()
            info['date'] = item.css('pubDate::text').extract_first()
            info['link'] = item.css('link::text').extract_first()
            next_page = item.css('link::text').extract_first()
            print(next_page)
            if next_page is not None:
                request = scrapy.Request(next_page,
                                 callback=self.parse_page2)
                request.meta['info'] = info
                yield request
            else:
                yield info

    def parse_page2(self, response):
        info = response.meta['info']
        yield info
