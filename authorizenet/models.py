from django.db import models

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
    ('7', 'CAVV attempt - failed validation - issuer available (U.S.-issued card/non-U.S acquirer)'),
    ('8', 'CAVV attempt - passed validation - issuer available (U.S.-issued card/non-U.S. acquirer)'),
    ('9', 'CAVV attempt - failed validation - issuer unavailable (U.S.-issued card/non-U.S. acquirer)'),
    ('A', 'CAVV attempt - passed validation - issuer unavailable (U.S.-issued card/non-U.S. acquirer)'),
    ('B', 'CAVV passed validation, information only, no liability shift'),
)


class ResponseManager(models.Manager):
    def create_from_dict(self, params):
        kwargs = dict(map(lambda x: (str(x[0][2:]), x[1]), params.items()))
        return self.create(**kwargs)

    def create_from_list(self, items):
        kwargs = dict(zip(map(lambda x: x.name, Response._meta.fields)[1:], items))
        return self.create(**kwargs)


class Response(models.Model):
    response_code = models.CharField(max_length=2, choices=RESPONSE_CHOICES)
    response_subcode = models.CharField(max_length=10)
    response_reason_code = models.CharField(max_length=15)
    response_reason_text = models.TextField()
    auth_code = models.CharField(max_length=10)
    avs_code = models.CharField(max_length=10, choices=AVS_RESPONSE_CODE_CHOICES)
    trans_id = models.CharField(max_length=255, db_index=True)
    invoice_num = models.CharField(max_length=20, blank=True)
    description = models.CharField(max_length=255)
    amount = models.CharField(max_length=16)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, db_index=True)
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
    cvv2_resp_code = models.CharField(max_length=2, choices=CVV2_RESPONSE_CODE_CHOICES, blank=True)
    cavv_response = models.CharField(max_length=2, choices=CAVV_RESPONSE_CODE_CHOICES, blank=True)

    test_request = models.CharField(max_length=10, default="FALSE", blank=True)

    objects = ResponseManager()

    @property
    def is_approved(self):
        return self.response_code == '1'

    def __unicode__(self):
        return u"response_code: %s, trans_id: %s, amount: %s, type: %s" % (self.response_code, self.trans_id, self.amount, self.type)
