from comics.models import Comic, ComicStrip
from django.db.utils import IntegrityError

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
        comic.date = item['date']
        if 'title' in item:
            comic.title = item['title']
        else:
            comic.title = None

        if comic.title is None:
            comic.title = "{} : {}/{}/{}".format(
                    self.comic_strip.name,
                    comic.date.month,
                    comic.date.day,
                    comic.date.year)

        comic.comic_page_url = item['comic_page_url']
        comic.comic_url = item['comic_url']
        if 'alt_text' in item:
            comic.alt_text = item['alt_text']
        if 'alt_comic_url' in item:
            comic.alt_comic_url = item['alt_comic_url']
        try:
            comic.save()
        except IntegrityError:
            # Not needed, but we should try updating here. 
            pass

        return item
