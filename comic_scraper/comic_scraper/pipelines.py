from comics.models import Comic
import json

class ComicScraperPipeline(object):
    def __init__(self, unique_id, *args, **kwargs):
        self.unique_id = unique_id
        self.title = ''

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            unique_id=crawler.settings.get('unique_id'), # this will be passed from django view
        )

    def close_spider(self, spider):
        # And here we are saving our crawled data with django models.
        comic = Comic()
        comic.title = json.dumps(self.title)
        item.save()

    def process_item(self, item, spider):
        self.title = item['title']
        return item
    
