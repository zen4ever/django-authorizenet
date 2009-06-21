from django.shortcuts import render_to_response
from django.template import RequestContext

def sim_payment(request):
    return render_to_response('authorizenet/sim_payment.html', context_instance=RequestContext(request))
