from django.conf.urls import url

from . import views

app_name='comics'
urlpatterns = [
    url('', views.index, name='index'),
    url('(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/date/', views.date, name='date'),
    url('(?P<comic_strip_id>[0-9]+)/comic_strip/', views.comic_strip, name='comic_strip'),
    url('(?P<comic_id>[0-9]+)/comic/', views.comic, name='comic'),
    url('(?P<comic_strip_id>[0-9]+)/update/', views.update_comics, name='update_comics'),
    ]
