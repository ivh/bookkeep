from django.conf.urls.defaults import *

urlpatterns = patterns('bkweb.bk.views',
                       (r'^$', 'index'),
                       (r'^account/$', 'accounts'),
                       (r'^balance/$', 'balance'),
                       (r'^result/$', 'result'),
                       (r'^recalc/$', 'recalc'),
                       (r'^ledger/$', 'ledger'),
                       (r'^account/(?P<accno>\d+)/$', 'account'),
                       (r'^transaction/(?P<transid>\d+)/$', 'transaction'),
                       (r'^invoice/(?P<transid>\d+)/$', 'invoice'),
                       (r'^invoice/(?P<invid>\d+)/$', 'invoice'),
                       (r'^invoice/(?P<invid>\d+)/pay$', 'pay_invoice'),
                       
)
