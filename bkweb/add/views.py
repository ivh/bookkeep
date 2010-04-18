from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from bkweb.bk.models import Account,Booking,Transaction,Counterpart,Invoice
from bkweb.settings import VAT_RATES
from datetime import date

def index(request):
    c=RequestContext(request,{})
    return render_to_response('add/index.html', c)

def counterpart(request):
    if 'pressed' in request.POST.keys():
        try:
            cp=Counterpart(isCustomer=(request.POST['choice'] == 'customer'),name=request.POST['name'])
            cp.save()
            return HttpResponseRedirect(reverse('bkweb.add.views.customer'))
        except:
            c=RequestContext(request,{'error_message':_('Please fill out everything!')})
            return render_to_response('add/customer.html', c)
    else:
        c=RequestContext(request,{})
        return render_to_response('add/customer.html', c)

def customerinv(request):
    accs=Account.objects.all()
    payaccs=[accs.get(accno=1930),accs.get(accno=2013)] #1930 2013
    whataccs=[accs.get(accno=3000),accs.get(accno=3100)] # 3000 3100
    counterps=Counterpart.objects.filter(isCustomer=True)
    
    c = RequestContext(request,{'error_message':_('Something went wrong!'),
                                'vats':VAT_RATES,
                                'whataccs':whataccs,
                                'payaccs':payaccs,
                                'counterps':counterps,
                                'date':date.today().isoformat(),
                                })
    return render_to_response('add/customerinv.html', c)


def customerinv_recieve(request):
    p=request.POST
    try:
        cpid=p['counterp']
        date=p['date']
        amount=float(p['amount'])
        vat=float(p['vat'])
        descr=p['descr']
        whatid=p['what']
        paidid=p['paidfrom']
        
        brutto=amount/(1.0+(vat/100.0))
        vat=amount-brutto
    
        #print amount,brutto,vat
        #print whatid,paidid,descr
        
        cp=get_object_or_404(Counterpart,id=cpid)
        outvat_acc=get_object_or_404(Account,accno=2610)
        claims_acc=get_object_or_404(Account,accno=1500)
        what_acc=get_object_or_404(Account,accno=whatid)
        
        trans=Transaction(date=date,description=u'%s: %s'%(_('Invoice'),descr))
        trans.save()
        Booking(trans=trans,acc=outvat_acc,credit=vat).save()
        Booking(trans=trans,acc=claims_acc,debit=amount).save()
        Booking(trans=trans,acc=what_acc,credit=brutto).save()
        
        inv=Invoice(date=date, counterpart=cp, trans=trans, description=descr)
        inv.save()
        return HttpResponseRedirect(reverse('bkweb.add.views.customerinv'))

    except:
        return HttpResponseRedirect(reverse('bkweb.add.views.customerinv'))

    
    
def supplierinv(request):
    accs=Account.objects
    payaccs=[accs.get(accno=1930),accs.get(accno=2017)]
    whataccs=[accs.get(accno=1220)]
    for acc in accs.filter(accno__gte=4000).filter(accno__lt=7000):
        whataccs.append(acc)

    counterps=Counterpart.objects.filter(isCustomer=False)
    
    c = RequestContext(request,{'error_message':_('Something went wrong!'),
                                'vats':VAT_RATES,
                                'whataccs':whataccs,
                                'payaccs':payaccs,
                                'counterps':counterps,
                                'date':date.today().isoformat(),
                                })
        
    try:
        cp=Counterpart
        trans=Transaction()
            
        inv=Invoice(date=date, isCustomer=True, counterpart=cp, trans=trans, description=trans.description, )
        inv.save()
        return HttpResponseRedirect(reverse('bkweb.add.views.customer'))
    except:
        return render_to_response('add/supplierinv.html', c)
