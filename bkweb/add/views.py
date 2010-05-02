from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext, Context
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django import forms
from django.db.models import Q

from bkweb.bk.models import Account,Booking,Transaction,Counterpart,Invoice
from datetime import date as DATE
from decimal import Decimal as D
######### GLOBALS
VAT_RATES = [
    (D('0.25'),'25 %'),
    (D('0.12'),'12 %'),
    (D('0.06'),'6 %'),
    (D('0.0'),'0 %'),
]

outvat_acc=Account.objects.get(pk=2610)
invat_acc=Account.objects.get(pk=2640)
outvateu_acc=Account.objects.get(pk=2614)
invateu_acc=Account.objects.get(pk=2645)

currloss_acc=Account.objects.get(pk=7960)

claims_acc=Account.objects.get(accno=1500)
suppdept_acc=Account.objects.get(accno=2440)

payaccounts=Account.objects.filter(pk__in=[1930,2010])
sellfrom_accounts=Account.objects.filter(pk__in=[3000,3100])

buyfrom_Qs=(Q(accno__lt=7000) & Q(accno__gte=4000)) | Q(accno=1220)
buyfrom_accounts=Account.objects.filter(buyfrom_Qs)
######### FORMS


class CounterpForm(forms.ModelForm):
    class Meta:
        model=Counterpart

class CustInvForm(forms.Form):
    date=forms.DateField(label=_('Date'),initial=DATE.today())
    customer=forms.ChoiceField(label=_('Customer'),choices=Counterpart.objects.filter(isCustomer=True).order_by('name').values_list('id','name'))
    amount=forms.DecimalField(label=_('Gross amount'))
    plusvat=forms.ChoiceField(label=_('plus VAT'),choices=VAT_RATES)
    descr=forms.CharField(label=_('Description'),min_length=5,max_length=512)
    what=forms.ChoiceField(label=_('What was sold?'),choices=sellfrom_accounts.values_list('accno','description'))
    payed=forms.ChoiceField(label=_('Paid to'),choices=[('','')] + list(payaccounts.values_list('accno','description')),required=False)
    paydate=forms.DateField(label=_('Date'),initial=DATE.today())
    payedamount=forms.DecimalField(label=_('Actual Amout'),help_text=_('If the is a currency gain/loss, write the amount here that was actually paid.'),required=False)
    calcvat=forms.ChoiceField(label=_('Non-paid VAT?'),help_text=_('In case of EU-transaction, no VAT is paid, but needs to be accounted for.'),choices=VAT_RATES[::-1])

class SuppInvForm(forms.Form):
    date=forms.DateField(label=_('Date'),initial=DATE.today())
    supplier=forms.ChoiceField(label=_('Supplier'),choices=Counterpart.objects.filter(isCustomer=False).order_by('name').values_list('id','name'))
    amount=forms.DecimalField(label=_('Amount'))
    includesvat=forms.ChoiceField(label=_('Included VAT'),choices=VAT_RATES)
    descr=forms.CharField(label=_('Description'),min_length=5,max_length=512)
    what=forms.ChoiceField(label=_('What was bought?'),choices=buyfrom_accounts.values_list('accno','description'))
    payed=forms.ChoiceField(label=_('Paid from'),choices=[('','')] + list(payaccounts.values_list('accno','description')),required=False)
    paydate=forms.DateField(label=_('Date'),initial=DATE.today())
    payedamount=forms.DecimalField(label=_('Actual Amout'),help_text=_('If the is a currency gain/loss, write the amount here that was actually paid.'),required=False)
    calcvat=forms.ChoiceField(label=_('Non-paid VAT?'),help_text=_('In case of EU-transaction, no VAT is paid, but needs to be accounted for.'),choices=VAT_RATES[::-1])



############################


def index(request):
    c=RequestContext(request,{})
    return render_to_response('add/index.html', c)

def counterpart(request):
    if request.method == 'POST':
        counterp=CounterpForm(request.POST)
        if counterp.is_valid():
            counterp.save()
    else:
        counterp=CounterpForm()

    c=RequestContext(request,{'counterp':counterp})
    return render_to_response('add/counterp.html', c)

def customerinv(request):
    if request.method == 'POST':
        custinv=CustInvForm(request.POST)
        if custinv.is_valid():
            d=custinv.cleaned_data
            print d
            vat=D(d['plusvat'])*d['amount']
            netto=d['amount']+vat
            
            cp=Counterpart.objects.get(pk=d['customer'])
            what_acc=Account.objects.get(accno=d['what'])
        
            trans=Transaction(date=d['date'],description=u'%s: %s'%(_('Invoice'),d['descr']))
            trans.save(force_insert=True)
            
            if vat: Booking.objects.create(trans=trans,acc=outvat_acc,credit=vat)
            Booking.objects.create(trans=trans,acc=claims_acc,debit=netto)
            Booking.objects.create(trans=trans,acc=what_acc,credit=d['amount'])

            if D(d['calcvat']):
                cvat=D(d['calcvat'])*d['amount']
                Booking.objects.create(trans=trans,acc=outvateu_acc,credit=cvat)
                Booking.objects.create(trans=trans,acc=invateu_acc,debit=cvat)

            if d['payed']:
                pay_acc=Account.objects.get(pk=d['payed'])
                paytrans=Transaction(date=d['paydate'],description=u'%s: %s'%(_('Invoice Payment'),d['descr']))
                paytrans.save(force_insert=True)

                if d['payedamount']:
                    payedamount=d['payedamount']
                    currloss=netto-d['payedamount']
                    Booking.objects.create(trans=paytrans,acc=currloss_acc,debit=currloss)
                    
                else: payedamount=netto

                Booking.objects.create(trans=paytrans,acc=pay_acc,debit=payedamount)
                Booking.objects.create(trans=paytrans,acc=claims_acc,credit=netto)
            else: paytrans=None
            
            
            inv=Invoice(date=d['date'], counterpart=cp, trans=trans, paytrans=paytrans, description=d['descr'])
            inv.save(force_insert=True)

        c=RequestContext(request,{'form':custinv})
    
    else:
        custinv=CustInvForm()
        c=Context({'form':custinv})
         
    return render_to_response('add/customerinv.html', c)


    
    
def supplierinv(request):
    if request.method == 'POST':
        custinv=SuppInvForm(request.POST)
        if custinv.is_valid():
            d=custinv.cleaned_data
            print d
            brutto = d['amount'] / (1+D(d['includesvat']))
            vat = d['amount'] - brutto
            
            cp=Counterpart.objects.get(pk=d['supplier'])
            what_acc=Account.objects.get(pk=d['what'])
        
            trans=Transaction(date=d['date'],description=u'%s: %s'%(_('Invoice'),d['descr']))
            trans.save(force_insert=True)

            if vat: Booking.objects.create(trans=trans,acc=invat_acc,debit=vat)
            Booking.objects.create(trans=trans,acc=suppdept_acc,credit=d['amount'])
            Booking.objects.create(trans=trans,acc=what_acc,debit=brutto)

            if D(d['calcvat']):
                cvat=D(d['calcvat'])*d['amount']
                Booking.objects.create(trans=trans,acc=invateu_acc,credit=cvat)
                Booking.objects.create(trans=trans,acc=outvateu_acc,debit=cvat)

            if d['payed']:
                pay_acc=Account.objects.get(pk=d['payed'])
                paytrans=Transaction(date=d['paydate'],description=u'%s: %s'%(_('Invoice Payment'),d['descr']))
                paytrans.save(force_insert=True)

                if d['payedamount']: 
                    payedamount=d['payedamount']
                    currloss=d['payedamount']-d['amount']
                    Booking.objects.create(trans=paytrans,acc=currloss_acc,debit=currloss)
                    
                else: payedamount=d['amount']

                Booking.objects.create(trans=paytrans,acc=pay_acc,credit=payedamount)
                Booking.objects.create(trans=paytrans,acc=suppdept_acc,debit=d['amount'])

            else: paytrans=None
            
            inv=Invoice(date=d['date'], counterpart=cp, trans=trans, paytrans=paytrans, description=d['descr'])
            inv.save(force_insert=True)
            
        c=RequestContext(request,{'form':custinv})
    
    else:
        custinv=SuppInvForm()
        c=Context({'form':custinv})
         
    return render_to_response('add/supplierinv.html', c)
