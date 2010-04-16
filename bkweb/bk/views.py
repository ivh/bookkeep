# Create your views here.
from bkweb.bk.models import Account,Booking

from django.shortcuts import render_to_response
def index(request):
    account_list = Account.objects.all().order_by('accno')
    return render_to_response('bk/index.html', {'account_list': account_list})

def accounts(request):
    accs = Account.objects.all().order_by('accno')
    
    return render_to_response('bk/accounts.html', {'accounts': accs})

def balance(request):
    return render_to_response('bk/accounts.html', {'accounts': accs})

def result(request):
    return render_to_response('bk/accounts.html', {'accounts': accs})

def recalc(request):
    accs = Account.objects.all().order_by('accno')
    for acc in accs:
        balance=0.0
        for boo in acc.booking_set.all():
            if boo.debit:
                if acc.debinc: balance+=boo.debit
                else: balance-=boo.debit
            if boo.credit:
                if acc.debinc: balance-=boo.credit
                else: balance+=boo.credit
        acc.balance=balance
        acc.save()
    return render_to_response('bk/done.html', {})


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
