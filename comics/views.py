from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Comic, ComicStrip

from scrapyd_api import ScrapydAPI
# connect scrapyd service
scrapyd = ScrapydAPI('http://scrapyd:6800')

import datetime

def index(request):
    comic_strip_list = ComicStrip.objects.order_by('-name')
    context = {
        'comic_strip_list': comic_strip_list,
    }
    return render(request, 'comics/index.html', context)

def date(request, year, month, day):
    date = datetime.date(int(year), int(month), int(day))
    one_day = datetime.timedelta(days=1)
    comic_list = get_list_or_404(Comic.objects.order_by('title'), date=date)
    context = {
        'date' : date,
        'prev_date' : date - one_day,
        'next_date' : date + one_day,
        'comic_list' : comic_list,
    }
    return render(request, 'comics/date.html', context)

def comic_strip(request, comic_strip_id, message=None):
    comic_strip = get_object_or_404(ComicStrip, id=comic_strip_id)
    all_comics = comic_strip.comic_set.all().order_by('-date')
    context = {
        'comic_strip' : comic_strip,
        'comic_list': all_comics,
    }
    if message is not None:
        context['message'] = message
    return render(request, 'comics/comic_strip.html', context)

def comic(request, comic_id):
    comic = get_object_or_404(Comic, id=comic_id)
    context = {
        'comic' : comic,
    }
    return render(request, 'comics/comic.html', context)

def schedule_comic_update(my_comic_strip):
    if my_comic_strip.rss_feed is not '':
        url = my_comic_strip.rss_feed
    else:
        url = my_comic_strip.base_url

    settings = {
            'comic_strip' : my_comic_strip
            }

    task = scrapyd.schedule(
            'default', 
            my_comic_strip.scraper_name, 
            settings=settings, 
            url=url)
    return task

def update_comics(request, comic_strip_id):
    my_comic_strip = get_object_or_404(ComicStrip, id=comic_strip_id)
    schedule_comic_update(my_comic_strip)

    return comic_strip(request, comic_strip_id, "Update Scheduled")

def update_all_comics(request):
    for current_comic_strip in ComicStrip.objects.all():
        schedule_comic_update(current_comic_strip)

    return index(request)
