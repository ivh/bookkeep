from django.conf.urls.defaults import *

urlpatterns = patterns('bkweb.add.views',
                       (r'^$', 'index'),
                       (r'^counterpart/$', 'counterpart'),
                       (r'^customerinv/$', 'customerinv'),
                       (r'^supplierinv/$', 'supplierinv'),
                       )
