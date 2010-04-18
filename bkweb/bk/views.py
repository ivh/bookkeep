# Create your views here.
from bkweb.bk.models import Account,Booking,Transaction
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from datetime import date

def index(request):
    c=RequestContext(request,{})
    return render_to_response('bk/index.html', c)

def accounts(request):
    accs = Account.objects.all().order_by('accno')
    c=RequestContext(request, {'accounts': accs})
    return render_to_response('bk/accounts.html', c)

def _sum_accounts(accs):
    s=0.0
    for acc in accs:
        s+=acc.balance
    return s

def ledger(request):
    bookings=Booking.objects.all().order_by('id')
    c=RequestContext(request,{'bookings':bookings,
                              'date':date.today().isoformat(),
                              })
    return render_to_response('bk/ledger.html',c)

def balance(request):
    accs=Account.objects.all()
    assets=accs.filter(accno__gte=1000).filter(accno__lt=2000)
    equity=accs.filter(accno__gte=2000).filter(accno__lt=2300)
    liabs=accs.filter(accno__gte=2300).filter(accno__lt=3000)
    
    eqs=_sum_accounts(equity)
    lis=_sum_accounts(liabs)
    ass=_sum_accounts(assets)
    c=RequestContext(request,{'assets':assets,
                               'liabilities':liabs,
                               'equity':equity,
                               'asset_sum':ass,
                               'liab_sum':lis,
                               'equity_sum':eqs,
                               'date':date.today().isoformat(),
                               })
    return render_to_response('bk/balance.html',c)

def result(request):
    accs=Account.objects.all()
    incomes=accs.filter(accno__gte=3000).filter(accno__lt=4000)
    expenses=accs.filter(accno__gte=4000).filter(accno__lt=9000)

    income=_sum_accounts(incomes)
    expense=_sum_accounts(expenses)
    incomeloss=income-expense
    c=RequestContext(request,{'expenses': expenses,
                               'incomes':incomes,
                               'expense': expense,
                               'income':income,
                               'incomeloss':incomeloss,
                               'date':date.today().isoformat()
                               })
    return render_to_response('bk/result.html',c)

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
    return HttpResponseRedirect(reverse('bkweb.bk.views.accounts'))

def account(request,accno):
    acc=get_object_or_404(Account,accno=accno)
    bookings=Booking.objects.filter(acc=accno).order_by('id')
    c=RequestContext(request,{'bookings':bookings,
                              'date':date.today().isoformat(),
                              'acc':acc,
                              })
    return render_to_response('bk/account.html', c)

def transaction(request,transid):
    trans=get_object_or_404(Transaction,id=transid)
    bookings=Booking.objects.filter(trans=transid).order_by('id')
    c=RequestContext(request,{'bookings':bookings,
                              'date':date.today().isoformat(),
                              'trans':trans,
                              })
    return render_to_response('bk/transaction.html', c)
    

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
