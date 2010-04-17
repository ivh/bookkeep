from bkweb.bk.models import Account,Booking,Transaction
from django.shortcuts import render_to_response
from django.template import RequestContext

from datetime import date

def index(request):
    c=RequestContext(request,{})
    return render_to_response('add/index.html', c)
