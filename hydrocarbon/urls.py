from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hydrocarbon.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'', include('board.urls.default')),
    url(r'^admin/', include(admin.site.urls)),
)

handler403 = 'board.urls.default.handler403'
