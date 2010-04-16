from django.conf.urls.defaults import *

urlpatterns = patterns('bkweb.bk.views',
                       (r'^$', 'index'),
                       (r'^accounts/$', 'accounts'),
                       (r'^balance/$', 'balance'),
                       (r'^result/$', 'result'),
                       (r'^recalc/$', 'recalc'),
)
