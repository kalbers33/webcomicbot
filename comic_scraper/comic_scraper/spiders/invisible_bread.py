# -*- coding: utf-8 -*-
import scrapy
from dateutil.parser import parse


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
            # 'date' : '%a, %d %b %Y %H:%M:%S %z'
            info['date'] = parse(item.css('pubDate::text').extract_first())
            info['comic_page_url'] = item.css('link::text').extract_first()
            next_page = item.css('link::text').extract_first()
            if next_page is not None:
                request = scrapy.Request(next_page,
                                 callback=self.main_page)
                request.meta['info'] = info
                yield request

    def main_page(self, response):
        info = response.meta['info']
        comic_url = response.css("#comic-1 img::attr(src)").extract_first()
        info['comic_url'] = response.urljoin(comic_url)
        info['alt_text'] = response.css(".widget-content p::text").extract_first()

        next_page = response.css("#extrapanelbutton a::attr(href)").extract_first()
        if next_page is not None:
            request = scrapy.Request(
                    next_page,
                    callback=self.hidden_page)
            request.meta['info'] = info
            yield request

    def hidden_page(self, response):
        info = response.meta['info']
        alt_comic_url = response.css("#content img::attr(src)").extract_first()
        info['alt_comic_url'] = response.urljoin(alt_comic_url)
        yield info
