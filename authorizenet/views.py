from django.shortcuts import render_to_response
from django.template import RequestContext
from authorizenet.models import Response

def sim_payment(request):
    response = Response.objects.create_from_dict(request.POST)
    return render_to_response('authorizenet/sim_payment.html', context_instance=RequestContext(request))
