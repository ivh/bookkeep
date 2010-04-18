from django.conf.urls.defaults import *

urlpatterns = patterns('bkweb.add.views',
                       (r'^$', 'index'),
                       (r'^counterpart/$', 'counterpart'),
                       (r'^customerinv/$', 'customerinv'),
                       (r'^customerinv_recieve/$', 'customerinv_recieve'),
                       (r'^supplierinv/$', 'supplierinv'),
                       )
