
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as aviews

from blog import views as bv

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^s/$', bv.s),
    url(r'^login/$', aviews.login, name='login'),
    url(r'^logout/$', aviews.logout, name='logout')
]
