from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Comic, ComicStrip

import datetime

def index(request):
    comic_strip_list = ComicStrip.objects.order_by('-name')
    template = loader.get_template('comics/index.html')
    context = {
        'comic_strip_list': comic_strip_list,
    }
    return HttpResponse(template.render(context, request))

def date(request, year, month, day):
    date = datetime.date(int(year), int(month), int(day))
    comic_list = get_list_or_404(Comic, date=date)
    context = {
        'date' : date,
        'comic_list' : comic_list,
    }
    return render(request, 'comics/date.html', context)

def comic_strip(request, comic_strip_id, message=None):
    comic_strip = get_object_or_404(ComicStrip, id=comic_strip_id)
    all_comics = comic_strip.comic_set.all()
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

def update_comics(request, comic_strip_id):
    return comic_strip(request, comic_strip_id, "Updated!")
