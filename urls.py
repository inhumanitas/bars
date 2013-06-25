from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin
import os

admin.autodiscover()
site_static = os.path.join(
  os.path.dirname(__file__), 'templates'
)


urlpatterns = patterns('',
    url(r'^$', 'bars.news.views.hello'),
    url(r'^hello/', 'bars.news.views.hello'),
    url(r'^news/', 'bars.news.views.news'),
    url(r'^getlog/$', 'bars.upgmaker.views.getlog'),
    url(r'^log/', 'bars.upgmaker.views.log'),
    url(r'^runbranch/$', 'bars.upgmaker.views.runbranch'),
    url(r'^getChlists/$', 'bars.upgmaker.views.getChlists'),
    url(r'^upgmaker/', 'bars.upgmaker.views.upgmaker'),
    url(r'^knowledge/', 'bars.knowledge.views.knowledge'),
    url(r'^about/', 'bars.about.views.about'),
    url(r'^faq/', 'bars.faq.views.faq'),
    url( r'^accounts/login/$', 'django.contrib.auth.views.login', { "template_name": "accounts/login.html" } ),
    url( r'^accounts/logout/$','bars.accounts.views.doLogout'),
    url( r'^login/$', 'bars.accounts.views.doLogin'),
    url( r'^logout/$', 'bars.accounts.views.doLogout'),
    (r'^site_static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
)
