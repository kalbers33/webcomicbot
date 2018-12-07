# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from dateutil.parser import parse


class DilbertSpider(scrapy.Spider):
    name = 'dilbert'
    allowed_domains = ['feed.dilbert.com',
            'dilbert.com']
    start_urls = ['http://feed.dilbert.com/dilbert/daily_strip/']

    def parse(self, response):
        # I don't know why, but I need to explicity use Selector here. 
        for entry in Selector(text=response.text).css('entry'):
            for href in entry.css('link::attr(href)').extract():
                yield scrapy.Request(href, callback=self.comic_page)

    def comic_page(self, response):
        info = {}
        url = response.css('.img-comic-container .img-comic-link')
        url = url.css('img::attr(src)').extract_first()
        url = response.urljoin(url)
        info['comic_url'] = url
        info['title'] = response.css('.comic-title-name::text').extract_first()

        date = response.css('.comic-title-date span::text')[0].extract()
        date = date + response.css('.comic-title-date span::text')[1].extract()
        info['date'] = parse(date)
        info['comic_page_url'] = response.url
        return info

