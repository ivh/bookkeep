from django.conf.urls.defaults import *

urlpatterns = patterns('bkweb.bk.views',
                       (r'^$', 'index'),
                       (r'^kontoplan/$', 'kontoplan'),
)
