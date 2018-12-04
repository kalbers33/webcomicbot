from django.urls import path, re_path, include

from . import views

app_name='comics'
urlpatterns = [
    path('', views.index, name='index'),
    re_path('(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/date/', views.date, name='date'),
    re_path('(?P<comic_strip_id>[0-9]+)/comic_strip/', views.comic_strip, name='comic_strip'),
    re_path('(?P<comic_id>[0-9]+)/comic/', views.comic, name='comic'),
    re_path('(?P<comic_strip_id>[0-9]+)/update/', views.update_comics, name='update_comics'),
    ]
