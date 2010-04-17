from bkweb.bk.models import Account,Booking,Transaction,Counterpart,Invoice
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from datetime import date

def index(request):
    c=RequestContext(request,{})
    return render_to_response('add/index.html', c)

def customer(request):
    try:
        cp=Counterpart(request.POST['choice'] == 'customer',request.POST['name'])
        cp.save()
    except:
        render_to_response('add/customer.html', {'error_message':_('Please fill out everything!')})
    
    c=RequestContext(request,{})
    return render_to_response('add/customer.html', c)

def customerinv(request):
    c=RequestContext(request,{})
    return render_to_response('add/index.html', c)

def supplier(request):
    c=RequestContext(request,{})
    return render_to_response('add/index.html', c)

def supplierinv(request):
    c=RequestContext(request,{})
    return render_to_response('add/index.html', c)
