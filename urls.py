from django.conf.urls.defaults import patterns, include, url

import views
import jinja_views
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^index/', views.index),
    url(r'^jinja2/', jinja_views.jinja2),
    url(r'^home/', jinja_views.home),
    # url(r'^static/(?P<path>.*)$', 'pyutil.django.views.static.serve', {'document_root': settings.STATICFILES_DIR})
)

