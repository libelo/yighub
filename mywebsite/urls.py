from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^/$', 'yighub.views.home'),
    url(r'^yighub/', include('yighub.urls', namespace='yighub')),
    # Examples:
    # url(r'^$', 'new_YIG_website.views.home', name='home'),
    # url(r'^new_YIG_website/', include('new_YIG_website.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
