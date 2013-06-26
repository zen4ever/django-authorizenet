from django.db import models
from django.forms.models import model_to_dict

from .conf import settings
from .cim import add_profile, get_profile, update_payment_profile, \
    create_payment_profile, delete_profile, delete_payment_profile

from .managers import CustomerProfileManager, CustomerPaymentProfileManager
from .exceptions import BillingError


RESPONSE_CHOICES = (
    ('1', 'Approved'),
    ('2', 'Declined'),
    ('3', 'Error'),
    ('4', 'Held for Review'),
)

AVS_RESPONSE_CODE_CHOICES = (
    ('A', 'Address (Street) matches, ZIP does not'),
    ('B', 'Address information not provided for AVS check'),
    ('E', 'AVS error'),
    ('G', 'Non-U.S. Card Issuing Bank'),
    ('N', 'No Match on Address (Street) or ZIP'),
    ('P', 'AVS not applicable for this transaction'),
    ('R', 'Retry - System unavailable or timed out'),
    ('S', 'Service not supported by issuer'),
    ('U', 'Address information is unavailable'),
    ('W', 'Nine digit ZIP matches, Address (Street) does not'),
    ('X', 'Address (Street) and nine digit ZIP match'),
    ('Y', 'Address (Street) and five digit ZIP match'),
    ('Z', 'Five digit ZIP matches, Address (Street) does not'),
)

METHOD_CHOICES = (
    ('CC', 'Credit Card'),
    ('ECHECK', 'eCheck'),
)

TYPE_CHOICES = (
    ('auth_capture', 'Authorize and Capture'),
    ('auth_only', 'Authorize only'),
    ('credit', 'Credit'),
    ('prior_auth_capture', 'Prior capture'),
    ('void', 'Void'),
)

CVV2_RESPONSE_CODE_CHOICES = (
    ('M', 'Match'),
    ('N', 'No Match'),
    ('P', 'Not Processed'),
    ('S', 'Should have been present'),
    ('U', 'Issuer unable to process request'),
)

CAVV_RESPONSE_CODE_CHOICES = (
    ('', 'CAVV not validated'),
    ('0', 'CAVV not validated because erroneous data was submitted'),
    ('1', 'CAVV failed validation'),
    ('2', 'CAVV passed validation'),
    ('3', 'CAVV validation could not be performed; issuer attempt incomplete'),
    ('4', 'CAVV validation could not be performed; issuer system error'),
    ('5', 'Reserved for future use'),
    ('6', 'Reserved for future use'),
    ('7', 'CAVV attempt - failed validation - '
          'issuer available (U.S.-issued card/non-U.S acquirer)'),
    ('8', 'CAVV attempt - passed validation - '
          'issuer available (U.S.-issued card/non-U.S. acquirer)'),
    ('9', 'CAVV attempt - failed validation - '
          'issuer unavailable (U.S.-issued card/non-U.S. acquirer)'),
    ('A', 'CAVV attempt - passed validation - '
          'issuer unavailable (U.S.-issued card/non-U.S. acquirer)'),
    ('B', 'CAVV passed validation, information only, no liability shift'),
)


CIM_RESPONSE_CODE_CHOICES = (
    ('I00001', 'Successful'),
    ('I00003', 'The record has already been deleted.'),
    ('E00001', 'An error occurred during processing. Please try again.'),
    ('E00002', 'The content-type specified is not supported.'),
    ('E00003', 'An error occurred while parsing the XML request.'),
    ('E00004', 'The name of the requested API method is invalid.'),
    ('E00005', 'The merchantAuthentication.transactionKey '
               'is invalid or not present.'),
    ('E00006', 'The merchantAuthentication.name is invalid or not present.'),
    ('E00007', 'User authentication failed '
               'due to invalid authentication values.'),
    ('E00008', 'User authentication failed. The payment gateway account or '
               'user is inactive.'),
    ('E00009', 'The payment gateway account is in Test Mode. '
               'The request cannot be processed.'),
    ('E00010', 'User authentication failed. '
               'You do not have the appropriate permissions.'),
    ('E00011', 'Access denied. You do not have the appropriate permissions.'),
    ('E00013', 'The field is invalid.'),
    ('E00014', 'A required field is not present.'),
    ('E00015', 'The field length is invalid.'),
    ('E00016', 'The field type is invalid.'),
    ('E00019', 'The customer taxId or driversLicense information '
               'is required.'),
    ('E00027', 'The transaction was unsuccessful.'),
    ('E00029', 'Payment information is required.'),
    ('E00039', 'A duplicate record already exists.'),
    ('E00040', 'The record cannot be found.'),
    ('E00041', 'One or more fields must contain a value.'),
    ('E00042', 'The maximum number of payment profiles '
               'for the customer profile has been reached.'),
    ('E00043', 'The maximum number of shipping addresses '
               'for the customer profile has been reached.'),
    ('E00044', 'Customer Information Manager is not enabled.'),
    ('E00045', 'The root node does not reference a valid XML namespace.'),
    ('E00051', 'The original transaction was not issued '
               'for this payment profile.'),
)


class ResponseManager(models.Manager):
    def create_from_dict(self, params):
        kwargs = dict(map(lambda x: (str(x[0][2:]), x[1]), params.items()))
        return self.create(**kwargs)

    def create_from_list(self, items):
        kwargs = dict(zip(map(lambda x: x.name,
                              Response._meta.fields)[1:], items))
        return self.create(**kwargs)


class Response(models.Model):
    response_code = models.CharField(max_length=2, choices=RESPONSE_CHOICES)
    response_subcode = models.CharField(max_length=10)
    response_reason_code = models.CharField(max_length=15)
    response_reason_text = models.TextField()
    auth_code = models.CharField(max_length=10)
    avs_code = models.CharField(max_length=10,
                                choices=AVS_RESPONSE_CODE_CHOICES)
    trans_id = models.CharField(max_length=255, db_index=True)
    invoice_num = models.CharField(max_length=20, blank=True)
    description = models.CharField(max_length=255)
    amount = models.CharField(max_length=16)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES)
    type = models.CharField(max_length=20,
                            choices=TYPE_CHOICES,
                            db_index=True)
    cust_id = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    address = models.CharField(max_length=60)
    city = models.CharField(max_length=40)
    state = models.CharField(max_length=40)
    zip = models.CharField(max_length=20)
    country = models.CharField(max_length=60)
    phone = models.CharField(max_length=25)
    fax = models.CharField(max_length=25)
    email = models.CharField(max_length=255)
    ship_to_first_name = models.CharField(max_length=50, blank=True)
    ship_to_last_name = models.CharField(max_length=50, blank=True)
    ship_to_company = models.CharField(max_length=50, blank=True)
    ship_to_address = models.CharField(max_length=60, blank=True)
    ship_to_city = models.CharField(max_length=40, blank=True)
    ship_to_state = models.CharField(max_length=40, blank=True)
    ship_to_zip = models.CharField(max_length=20, blank=True)
    ship_to_country = models.CharField(max_length=60, blank=True)
    tax = models.CharField(max_length=16, blank=True)
    duty = models.CharField(max_length=16, blank=True)
    freight = models.CharField(max_length=16, blank=True)
    tax_exempt = models.CharField(max_length=16, blank=True)
    po_num = models.CharField(max_length=25, blank=True)
    MD5_Hash = models.CharField(max_length=255)
    cvv2_resp_code = models.CharField(max_length=2,
                                      choices=CVV2_RESPONSE_CODE_CHOICES,
                                      blank=True)
    cavv_response = models.CharField(max_length=2,
                                     choices=CAVV_RESPONSE_CODE_CHOICES,
                                     blank=True)

    test_request = models.CharField(max_length=10, default="FALSE", blank=True)

    card_type = models.CharField(max_length=10, default="", blank=True)
    account_number = models.CharField(max_length=10, default="", blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    objects = ResponseManager()

    @property
    def is_approved(self):
        return self.response_code == '1'

    def __unicode__(self):
        return u"response_code: %s, trans_id: %s, amount: %s, type: %s" % \
                (self.response_code, self.trans_id, self.amount, self.type)


class CIMResponse(models.Model):
    result = models.CharField(max_length=8)
    result_code = models.CharField(max_length=8,
                                   choices=CIM_RESPONSE_CODE_CHOICES)
    result_text = models.TextField()
    transaction_response = models.ForeignKey(Response, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    @property
    def success(self):
        return self.result == 'Ok'

    def raise_if_error(self):
        if not self.success:
            raise BillingError(self.result_text)


class CustomerProfile(models.Model):

    """Authorize.NET customer profile"""

    customer = models.OneToOneField(settings.CUSTOMER_MODEL,
                                    related_name='customer_profile')
    profile_id = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        data = kwargs.pop('data', {})
        sync = kwargs.pop('sync', True)
        if not self.id and sync:
            self.push_to_server(data)
        super(CustomerProfile, self).save(*args, **kwargs)

    def delete(self):
        """Delete the customer profile remotely and locally"""
        response = delete_profile(self.profile_id)
        response.raise_if_error()
        super(CustomerProfile, self).delete()

    def push_to_server(self, data):
        output = add_profile(self.customer.pk, data, data)
        output['response'].raise_if_error()
        self.profile_id = output['profile_id']
        self.payment_profile_ids = output['payment_profile_ids']

    def sync(self):
        """Overwrite local customer profile data with remote data"""
        output = get_profile(self.profile_id)
        output['response'].raise_if_error()
        for payment_profile in output['payment_profiles']:
            instance, created = CustomerPaymentProfile.objects.get_or_create(
                customer_profile=self,
                payment_profile_id=payment_profile['payment_profile_id']
            )
            instance.sync(payment_profile)

    objects = CustomerProfileManager()

    def __unicode__(self):
        return self.profile_id


class CustomerPaymentProfile(models.Model):

    """Authorize.NET customer payment profile"""

    customer = models.ForeignKey(settings.CUSTOMER_MODEL,
                                 related_name='payment_profiles')
    customer_profile = models.ForeignKey('CustomerProfile',
                                         related_name='payment_profiles')
    payment_profile_id = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    company = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=25, blank=True)
    fax_number = models.CharField(max_length=25, blank=True)
    address = models.CharField(max_length=60, blank=True)
    city = models.CharField(max_length=40, blank=True)
    state = models.CharField(max_length=40, blank=True)
    zip = models.CharField(max_length=20, blank=True, verbose_name="ZIP")
    country = models.CharField(max_length=60, blank=True)
    card_number = models.CharField(max_length=16, blank=True)
    expiration_date = models.DateField(blank=True, null=True)
    card_code = None

    def __init__(self, *args, **kwargs):
        self.card_code = kwargs.pop('card_code', None)
        return super(CustomerPaymentProfile, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        if kwargs.pop('sync', True):
            self.push_to_server()
        self.card_code = None
        self.card_number = "XXXX%s" % self.card_number[-4:]
        super(CustomerPaymentProfile, self).save(*args, **kwargs)

    def push_to_server(self):
        if not self.customer_profile_id:
            try:
                self.customer_profile = CustomerProfile.objects.get(
                    customer=self.customer)
            except CustomerProfile.DoesNotExist:
                pass
        if self.payment_profile_id:
            response = update_payment_profile(
                self.customer_profile.profile_id,
                self.payment_profile_id,
                self.raw_data,
                self.raw_data,
            )
        elif self.customer_profile_id:
            output = create_payment_profile(
                self.customer_profile.profile_id,
                self.raw_data,
                self.raw_data,
            )
            response = output['response']
            self.payment_profile_id = output['payment_profile_id']
        else:
            output = add_profile(
                self.customer.id,
                self.raw_data,
                self.raw_data,
            )
            response = output['response']
            self.customer_profile = CustomerProfile.objects.create(
                customer=self.customer,
                profile_id=output['profile_id'],
                sync=False,
            )
            self.payment_profile_id = output['payment_profile_ids'][0]
        response.raise_if_error()

    @property
    def raw_data(self):
        """Return data suitable for use in payment and billing forms"""
        data = model_to_dict(self)
        data['card_code'] = getattr(self, 'card_code')
        return data

    def sync(self, data):
        """Overwrite local customer payment profile data with remote data"""
        for k, v in data.get('billing', {}).items():
            setattr(self, k, v)
        self.card_number = data.get('credit_card', {}).get('card_number',
                                                           self.card_number)
        self.save(sync=False)

    def delete(self):
        """Delete the customer payment profile remotely and locally"""
        response = delete_payment_profile(self.customer_profile.profile_id,
                                          self.payment_profile_id)
        response.raise_if_error()
        return super(CustomerPaymentProfile, self).delete()

    def update(self, **data):
        """Update the customer payment profile remotely and locally"""
        for key, value in data.items():
            setattr(self, key, value)
        self.save()
        return self

    def __unicode__(self):
        return self.payment_profile_id

    objects = CustomerPaymentProfileManager()
