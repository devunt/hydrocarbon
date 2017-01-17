from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'', include('board.urls.default')),
    url(r'^admin/', include(admin.site.urls)),
]

handler400 = 'board.urls.default.handler400'
handler403 = 'board.urls.default.handler403'
handler404 = 'board.urls.default.handler404'
handler500 = 'board.urls.default.handler500'
