from django.conf.urls import url

from .views import comment_thread


urlpatterns = [

    url(r'^(?P<abc>\d+)/$', comment_thread, name='thread'),
    # url(r'^(?P<id>[\w-]+)/del/$', comment_delete, name='delete'),

]
