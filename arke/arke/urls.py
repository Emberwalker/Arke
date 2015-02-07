from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'arke.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'votes.views.index', name='index'),
    url(r'^login/?$', 'votes.views.login', name='login'),
    url(r'^admin/', include(admin.site.urls)),
)
