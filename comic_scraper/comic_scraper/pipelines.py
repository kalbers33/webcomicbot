from comics.models import Comic, ComicStrip

class ComicScraperPipeline(object):
    def __init__(self, comic_strip, *args, **kwargs):
        self.comic_strip = comic_strip

    @classmethod
    def from_crawler(cls, crawler):
        my_comic_strip = ComicStrip.objects.get(name=crawler.settings.get('comic_strip'))
        return cls(
                comic_strip=my_comic_strip, # this will be passed from django view
        )

    def process_item(self, item, spider):
        comic = Comic()
        comic.comic_strip = self.comic_strip
        comic.title = item['title']
        comic.date = item['date']
        comic.alt_text = item['alt_text']
        comic.comic_page_url = item['comic_page_url']
        comic.comic_url = item['comic_url']
        comic.alt_comic_url = item['alt_comic_url']
        comic.save()
        return item
