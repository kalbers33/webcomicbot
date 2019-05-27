# -*- coding: utf-8 -*-
import scrapy
from dateutil.parser import parse

NUM_PAGES_TO_SCRAPE = 10

class ComicsKingdomSpider(scrapy.Spider):
    name = 'comics_kingdom'
    allowed_domains = ['comicskingdom.com', 'safr.kingfeatures.com']
    start_urls = ['http://comicskingdom.com/']

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.start_urls = [self.url]
        self.pages_scraped = 0

        super(ComicsKingdomSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        comic_page_url = response.css("slider-disqus::attr(date-slug)").extract_first()
        comic_page_url = response.urljoin("{}/{}".format(response.url, comic_page_url))

        yield scrapy.Request(
                comic_page_url,
                callback=self.parse_comic_page)

    def parse_comic_page(self, response):
        info = {}
        info['comic_page_url'] = response.url
        info['comic_url'] = response.css('slider-image::attr(image-url)').extract_first()
        date = response.css('slider-disqus::attr(date-slug)').extract_first()
        info['date'] = parse(date)
        self.pages_scraped = self.pages_scraped + 1
        yield info

        if self.pages_scraped < NUM_PAGES_TO_SCRAPE:
            next_date_string = response.css("slider-arrow[\:is-left-arrow=true]::attr(date-slug)").extract_first()
            next_page = response.urljoin(next_date_string)
            yield scrapy.Request(
                    next_page,
                    callback=self.parse_comic_page)
