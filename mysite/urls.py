from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as aviews
from django.conf import settings
from django.conf.urls.static import static

from blog import views as bv

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', aviews.login, name='login'),
    url(r'^logout/$', aviews.logout, name='logout'),
    url(r'^b/', include("blog.urls", namespace='posts'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


