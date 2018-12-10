# -*- coding: utf-8 -*-
import scrapy
from dateutil.parser import parse

NUM_PAGES_TO_SCRAPE = 10


class GocomicsSpider(scrapy.Spider):
    name = 'gocomics'
    allowed_domains = ['www.gocomics.com']
    start_urls = ['http://www.gocomics.com/']

    
    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.start_urls = [self.url]
        self.pages_scraped = 0

        super(GocomicsSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        comic_url = response.css("a.nav-link[data-link=comics]::attr(href)").extract_first()
        comic_url = response.urljoin(comic_url)

        yield scrapy.Request(
                comic_url,
                callback=self.parse_comic_page)

    def parse_comic_page(self, response):
        info = {}
        info['comic_page_url'] = response.url
        info['comic_url'] = response.css('picture.item-comic-image img::attr(src)').extract_first()
        date = response.css('.cal.off.calendar-input.datepicker::attr(placeholder)').extract_first()
        info['date'] = parse(date)
        self.pages_scraped = self.pages_scraped + 1
        yield info

        if self.pages_scraped < NUM_PAGES_TO_SCRAPE:
            next_page = response.css('a.fa.btn.btn-outline-secondary.btn-circle.fa-caret-left.sm.js-previous-comic::attr(href)').extract_first()
            next_page = response.urljoin(next_page)
            yield scrapy.Request(
                    next_page,
                    callback=self.parse_comic_page)


