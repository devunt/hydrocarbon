from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'', include('board.urls.default')),
    url(r'^admin/', include(admin.site.urls)),
]

handler403 = 'board.urls.default.handler403'
