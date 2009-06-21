import time
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from authorizenet.forms import SIMPaymentForm, AUTHNET_POST_URL, AUTHNET_TEST_POST_URL
from authorizenet.utils import get_fingerprint

def make_payment(request, invoice_id):
    if request.method=='GET':
        domain = Site.objects.get_current().domain
        params = {
            'x_amount' : '100.00',
            'x_fp_sequence' : invoice_id,
            'x_invoice_num' : invoice_id,
            'x_fp_timestamp' : str(int(time.time())),
            'x_relay_url' : "http://"+domain+reverse("authnet_sim_payment"),
            }

        params['x_fp_hash'] = get_fingerprint(invoice_id, params['x_fp_timestamp'], params['x_amount'])
        form = SIMPaymentForm(initial=params)
        if settings.DEBUG:
            post_url = AUTHNET_TEST_POST_URL
        else:
            post_url = AUTHNET_POST_URL
        return render_to_response('samplestore/make_payment.html', {'form':form, 'post_url':post_url}, context_instance=RequestContext(request))

