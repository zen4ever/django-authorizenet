import time
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from authorizenet.models import Response
from authorizenet.forms import SIMPaymentForm, SIMBillingForm
from authorizenet import AUTHNET_POST_URL, AUTHNET_TEST_POST_URL
from authorizenet.utils import get_fingerprint, capture_transaction
from samplestore.models import Invoice, Item, Address
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404

def items(request):
    return render_to_response('samplestore/items.html', {'items':Item.objects.all()}, context_instance=RequestContext(request))

@login_required
def commit_to_buy(request, item_id): 
    item = get_object_or_404(Item, id=item_id) 
    if request.POST:
        if "yes" in request.POST:
            invoice = Invoice.objects.create(customer=request.user.get_profile(), item=item)
            return HttpResponseRedirect(reverse('samplestore_make_payment', args=[invoice.id]))
        else:
            return HttpResponseRedirect(reverse('samplestore_items'))
    return render_to_response('samplestore/commit_to_buy.html', {'item':item}, context_instance=RequestContext(request))

@login_required
def make_payment(request, invoice_id):
    domain = Site.objects.get_current().domain
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if invoice.customer.user != request.user:
        raise Http404
    params = {
        'x_amount' : "%.2f" % invoice.item.price,
        'x_fp_sequence': invoice_id,
        'x_invoice_num': invoice_id,
        'x_description': invoice.item.title,
        'x_fp_timestamp' : str(int(time.time())),
        'x_relay_url' : "http://"+domain+reverse("authnet_sim_payment"),
        }

    try:
        ba = invoice.customer.address_set.get(type='billing')
        billing_params = {'x_first_name': ba.first_name, 
                          'x_last_name': ba.last_name,
                          'x_company': ba.company,
                          'x_address': ba.address,
                          'x_city': ba.city,
                          'x_state': ba.state,
                          'x_zip': ba.zip_code,
                          'x_country': "United States",
                          'x_phone': ba.phone,
                          'x_fax': ba.fax,
                          'x_email': request.user.email,
                          'x_cust_id': invoice.customer.id }
        billing_form = SIMBillingForm(initial=billing_params)
    except Address.DoesNotExist:
        billing_form = None 

    params['x_fp_hash'] = get_fingerprint(invoice_id, params['x_fp_timestamp'], params['x_amount'])
    form = SIMPaymentForm(initial=params)
    if settings.DEBUG:
        post_url = AUTHNET_TEST_POST_URL
    else:
        post_url = AUTHNET_POST_URL
    return render_to_response('samplestore/make_payment.html', {'form':form, 'billing_form':billing_form, 'post_url':post_url}, context_instance=RequestContext(request))

@login_required
def create_invoice(request, item_id, auth_only=False):
    item = get_object_or_404(Item, id=item_id)
    invoice = Invoice.objects.create(item=item, customer=request.user.get_profile())
    if auth_only:
        final_url = reverse('samplestore_make_direct_payment_auth', args=[invoice.id])
    else:
        final_url = reverse('samplestore_make_direct_payment', args=[invoice.id])
    return HttpResponseRedirect(final_url)

@login_required
def make_direct_payment(request, invoice_id, auth_only=False):
    domain = Site.objects.get_current().domain
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if invoice.customer.user != request.user:
        raise Http404
    try:
        ba = invoice.customer.address_set.get(type='billing')
        initial_data = {'first_name': ba.first_name, 
                        'last_name': ba.last_name,
                        'company': ba.company,
                        'address': ba.address,
                        'city': ba.city, 
                        'state': ba.state,
                        'zip': ba.zip_code }
        extra_data = { 'phone': ba.phone,
                       'fax': ba.fax,
                       'email': request.user.email,
                       'cust_id': invoice.customer.id }
    except Address.DoesNotExist:
        initial_data = {}
        extra_data = {} 
    if auth_only:
        extra_data['type'] = 'AUTH_ONLY'
    extra_data['amount'] = "%.2f" % invoice.item.price
    extra_data['invoice_num'] = invoice.id
    extra_data['description'] = invoice.item.title
    from authorizenet.views import AIMPayment
    pp = AIMPayment(extra_data=extra_data, context={'item':invoice.item}, initial_data=initial_data)
    return pp(request)

@login_required
def capture_index(request):
    responses = Response.objects.filter(type='auth_only')
    if request.user.is_staff:
        return render_to_response('samplestore/capture_index.html', {'responses':responses}, context_instance=RequestContext(request))
    raise Http404

@login_required
def capture(request, id):
    response = get_object_or_404(Response, id=id, type='auth_only')
    if Response.objects.filter(trans_id=response.trans_id, type='prior_auth_capture').count()>0:
        raise Http404
    if request.user.is_staff:
        new_response = capture_transaction(response)
        return render_to_response('samplestore/capture.html', {'response': response, 'new_response': new_response}, context_instance=RequestContext(request))
    raise Http404
