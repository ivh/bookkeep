# Create your views here.
from bkweb.bk.models import Account,Booking

from django.shortcuts import render_to_response
def index(request):
    account_list = Account.objects.all().order_by('accno')
    return render_to_response('bk/index.html', {'account_list': account_list})

def kontoplan(request):
    accounts = Account.objects.all().order_by('accno')
    
    return render_to_response('bk/kontoplan.html', {'accounts': accounts})


# long version
#from django.http import HttpResponse
#from django.template import Context, loader
#def index(request):
#    account_list = Account.objects.all().order_by('accno')
#    t = loader.get_template('bk/index.html')
#    c = Context({
#        'account_list': account_list,
#    })
#    return HttpResponse(t.render(c))
