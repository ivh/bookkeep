# Create your views here.
from bkweb.bk.models import Account,Booking
from django.shortcuts import render_to_response
from datetime import date
def index(request):
    account_list = Account.objects.all().order_by('accno')
    return render_to_response('index.html', {'account_list': account_list})

def accounts(request):
    accs = Account.objects.all().order_by('accno')
    
    return render_to_response('bk/accounts.html', {'accounts': accs})

def _sum_accounts(accs):
    s=0.0
    for acc in accs:
        s+=acc.balance
    return s

def balance(request):
    accs=Account.objects.all()
    assets=accs.filter(accno__gte=1000).filter(accno__lt=2000)
    equity=accs.filter(accno__gte=2000).filter(accno__lt=2300)
    liabs=accs.filter(accno__gte=2300).filter(accno__lt=3000)
    
    eqs=_sum_accounts(equity)
    lis=_sum_accounts(liabs)
    ass=_sum_accounts(assets)
    
    return render_to_response('bk/balance.html',
                              {'assets':assets,
                               'liabilities':liabs,
                               'equity':equity,
                               'asset_sum':ass,
                               'liab_sum':lis,
                               'equity_sum':eqs,
                               'date':date.today().isoformat()
                               })

def result(request):
    accs=Account.objects.all()
    expenses=accs.filter(accno__gte=3000).filter(accno__lt=4000)
    incomes=accs.filter(accno__gte=4000).filter(accno__lt=9000)

    income=_sum_accounts(incomes)
    expense=_sum_accounts(expenses)
    incomeloss=income-expense
    
    return render_to_response('bk/result.html',
                              {'expenses': expenses,
                               'incomes':incomes,
                               'expense': expense,
                               'income':income,
                               'incomeloss':incomeloss,
                               'date':date.today().isoformat()
                               })

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
