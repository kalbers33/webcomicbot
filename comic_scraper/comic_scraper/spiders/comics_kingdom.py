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
        info = {}

        comic_page_url = response.css(".inner-comic-wrap img::attr(data-src)").extract_first()
        comic_page_url = response.urljoin(comic_page_url)
        info['comic_page_url'] = response.css("header h5 a::attr(href)").extract_first()
        info['comic_page_url'] = response.urljoin(info['comic_page_url'])

        nav_bar = response.css("nav.date-nav.clearfix.no-overlay")

        date = nav_bar.css("span.no-mobile::text").extract_first()
        info['date'] = parse(date)

        next_comic_url = nav_bar.xpath("//i[@class='fa fa-caret-left']/parent::a/@href").extract_first()
        next_comic_url = response.urljoin(next_comic_url)

        if comic_page_url is not None:
            request = scrapy.Request(
                    comic_page_url,
                    callback=self.parse_comic_src
                    )
            request.meta['info'] = info
            request.meta['next_comic_url'] = next_comic_url
            yield request

    def parse_comic_src(self, response):
        info = response.meta['info']
        info['comic_url'] = response.css("img::attr(src)").extract_first()
        info['comic_url'] = response.urljoin(info['comic_url'])

        next_page = response.meta['next_comic_url']

        self.pages_scraped = self.pages_scraped + 1

        yield info

        if next_page is not None:
            if self.pages_scraped < NUM_PAGES_TO_SCRAPE:
                yield scrapy.Request(
                        next_page,
                        callback=self.parse)
