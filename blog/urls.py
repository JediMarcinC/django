
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as aviews

from . import views as bv

urlpatterns = [
    url(r'^i/$', bv.index),
    url(r'^demo/$', bv.demo),
    # url(r'^some/$', "blog.views.some"),
    url(r'^(?P<id>\d{1})/$', bv.detail, name='detail'),
    url(r'^(?P<id>\d{1})/edit/$', bv.update, name='edit'),
    # url(r'^', bv.index),
    url(r'^new/$', bv.create_post)
]
