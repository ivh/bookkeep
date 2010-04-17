from django.conf.urls.defaults import *

urlpatterns = patterns('bkweb.add.views',
                       (r'^$', 'index'),
                       (r'^customer/$', 'customer'),
                       (r'^customerinv/$', 'customerinv'),
                       (r'^supplyer/$', 'supplyer'),
                       (r'^supplyerinv/$', 'supplyerinv'),
                       )
