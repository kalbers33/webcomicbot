from django.db import models

from django.utils import timezone

import datetime


class ComicStrip(models.Model):

    DEFAULT = 'default'
    SCRAPER_LIST = (
            (DEFAULT, 'Default'),
            ('invisible_bread', 'Invisible Bread'),
            ('dilbert', 'Dilbert'),
            )

    name = models.CharField(max_length=200)
    base_url = models.URLField(max_length=200)
    rss_feed = models.URLField(max_length=500, default='')
    scraper_name = models.CharField(max_length=100, choices=SCRAPER_LIST, default=DEFAULT)

    def __str__(self):
        return self.name


class Comic(models.Model):
    comic_strip = models.ForeignKey(ComicStrip, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date = models.DateField('date published')
    alt_text = models.TextField('alternate text')
    comic_page_url = models.URLField(max_length=500, default='', unique=True)
    comic_url = models.URLField(max_length=500)
    alt_comic_url = models.URLField(max_length=500, default='')

    def __str__(self):
        return self.title

    def was_published_recently(self):
                return self.date >= timezone.now().date() - datetime.timedelta(days=1)

