import re
import urllib2
import xml.dom.minidom

from django.utils.datastructures import SortedDict
from django.conf import settings

from authorizenet import AUTHNET_CIM_URL, AUTHNET_TEST_CIM_URL
from authorizenet.models import CIMResponse, Response
from authorizenet.signals import customer_was_created, customer_was_flagged, \
        payment_was_successful, payment_was_flagged


BILLING_FIELDS = ('firstName',
                  'lastName',
                  'company',
                  'address',
                  'city',
                  'state',
                  'zip',
                  'country',
                  'phoneNumber',
                  'faxNumber')

SHIPPING_FIELDS = ('firstName',
                   'lastName',
                   'company',
                   'address',
                   'city',
                   'state',
                   'zip',
                   'country')

CREDIT_CARD_FIELDS = ('cardNumber',
                      'expirationDate',
                      'cardCode')


def extract_form_data(data):
    """
    Convert all keys in data dictionary from underscore_format to
    camelCaseFormat and return the new dict
    """
    to_upper = lambda match: match.group(1).upper()
    to_camel = lambda x: re.sub("_([a-z])", to_upper, x)
    return dict(map(lambda x: (to_camel(x[0]), x[1]), data.items()))


def extract_payment_form_data(data):
    payment_data = extract_form_data(data)
    payment_data['expirationDate'] = \
            payment_data['expirationDate'].strftime('%Y-%m')
    return payment_data


def create_form_data(data):
    """
    Convert all keys in data dictionary from camelCaseFormat to
    underscore_format and return the new dict
    """
    to_lower = lambda match: "_" + match.group(1).lower()
    to_under = lambda x: re.sub("([A-Z])", to_lower, x)
    return dict(map(lambda x: (to_under(x[0]), x[1]), data.items()))


def add_profile(customer_id, payment_form_data, billing_form_data,
                shipping_form_data=None, customer_email=None,
                customer_description=None):
    """
    Add a customer profile with a single payment profile
    and return a tuple of the CIMResponse, profile ID,
    and single-element list of payment profile IDs.

    Arguments (required):
    customer_id -- unique merchant-assigned customer identifier
    payment_form_data -- dictionary with keys in CREDIT_CARD_FIELDS
    billing_form_data -- dictionary with keys in BILLING_FIELDS
    shipping_form_data -- dictionary with keys in SHIPPING_FIELDS

    Keyword Arguments (optional):
    customer_email -- customer email
    customer_description -- customer description
    """
    kwargs = {'customer_id': customer_id,
              'credit_card_data': extract_payment_form_data(payment_form_data),
              'billing_data': extract_form_data(billing_form_data),
              'customer_email': customer_email,
              'customer_description': customer_description}
    if shipping_form_data:
        kwargs['shipping_data'] = extract_form_data(shipping_form_data)
    helper = CreateProfileRequest(**kwargs)
    response = helper.get_response()
    info = helper.customer_info
    if response.success:
        profile_id = helper.profile_id
        payment_profile_ids = helper.payment_profile_ids
        shipping_profile_ids = helper.shipping_profile_ids
        customer_was_created.send(sender=response,
                                  customer_id=info.get("merchantCustomerId"),
                                  customer_description=info.get("description"),
                                  customer_email=info.get("email"),
                                  profile_id=helper.profile_id,
                                  payment_profile_ids=helper.payment_profile_ids)
    else:
        profile_id = None
        payment_profile_ids = None
        shipping_profile_ids = None
        customer_was_flagged.send(sender=response,
                                  customer_id=customer_id)
    return {'response': response,
            'profile_id': profile_id,
            'payment_profile_ids': payment_profile_ids,
            'shipping_profile_ids': shipping_profile_ids}


def update_payment_profile(profile_id,
                           payment_profile_id,
                           payment_form_data,
                           billing_form_data):
    """
    Update a customer payment profile and return the CIMResponse.

    Arguments:
    profile_id -- unique gateway-assigned profile identifier
    payment_profile_id -- unique gateway-assigned payment profile identifier
    payment_form_data -- dictionary with keys in CREDIT_CARD_FIELDS
    billing_form_data -- dictionary with keys in BILLING_FIELDS
    """
    payment_data = extract_payment_form_data(payment_form_data)
    billing_data = extract_form_data(billing_form_data)
    helper = UpdatePaymentProfileRequest(profile_id,
                                         payment_profile_id,
                                         billing_data,
                                         payment_data)
    response = helper.get_response()
    return response


def create_payment_profile(profile_id, payment_form_data, billing_form_data):
    """
    Create a customer payment profile and return a tuple of the CIMResponse and
    payment profile ID.

    Arguments:
    profile_id -- unique gateway-assigned profile identifier
    payment_form_data -- dictionary with keys in CREDIT_CARD_FIELDS
    billing_form_data -- dictionary with keys in BILLING_FIELDS
    """
    payment_data = extract_payment_form_data(payment_form_data)
    billing_data = extract_form_data(billing_form_data)
    helper = CreatePaymentProfileRequest(profile_id,
                                         billing_data,
                                         payment_data)
    response = helper.get_response()
    if response.success:
        payment_profile_id = helper.payment_profile_id
    else:
        payment_profile_id = None
    return {'response': response, 'payment_profile_id': payment_profile_id}


def delete_payment_profile(profile_id, payment_profile_id):
    """
    Delete a customer payment profile and return the CIMResponse.

    Arguments:
    profile_id -- unique gateway-assigned profile identifier
    payment_profile_id -- unique gateway-assigned payment profile identifier
    """
    helper = DeletePaymentProfileRequest(profile_id, payment_profile_id)
    response = helper.get_response()
    return response


def update_shipping_profile(profile_id,
                            shipping_profile_id,
                            shipping_form_data):
    """
    Update a customer shipping profile and return the CIMResponse.

    Arguments:
    profile_id -- unique gateway-assigned profile identifier
    shipping_profile_id -- unique gateway-assigned shipping profile identifier
    shipping_form_data -- dictionary with keys in SHIPPING_FIELDS
    """
    shipping_data = extract_form_data(shipping_form_data)
    helper = UpdateShippingProfileRequest(profile_id,
                                          shipping_profile_id,
                                          shipping_data)
    response = helper.get_response()
    return response


def create_shipping_profile(profile_id, shipping_form_data):
    """
    Create a customer shipping profile and return a tuple of the CIMResponse and
    shipping profile ID.

    Arguments:
    profile_id -- unique gateway-assigned profile identifier
    shipping_form_data -- dictionary with keys in SHIPPING_FIELDS
    """
    shipping_data = extract_form_data(shipping_form_data)
    helper = CreateShippingProfileRequest(profile_id,
                                          shipping_data)
    response = helper.get_response()
    if response.success:
        shipping_profile_id = helper.shipping_profile_id
    else:
        shipping_profile_id = None
    return {'response': response, 'shipping_profile_id': shipping_profile_id}


def delete_shipping_profile(profile_id, shipping_profile_id):
    """
    Delete a customer shipping profile and return the CIMResponse.

    Arguments:
    profile_id -- unique gateway-assigned profile identifier
    shipping_profile_id -- unique gateway-assigned shipping profile identifier
    """
    helper = DeleteShippingProfileRequest(profile_id, shipping_profile_id)
    response = helper.get_response()
    return response


def get_profile(profile_id):
    """
    Retrieve a customer payment profile from the profile ID and return a tuple
    of the CIMResponse and two lists of dictionaries containing data for each
    payment and shipping profile.

    Arguments:
    profile_id -- unique gateway-assigned profile identifier
    """
    helper = GetProfileRequest(profile_id)
    response = helper.get_response()
    return {'response': response,
            'payment_profiles': helper.payment_profiles,
            'shipping_profiles': helper.shipping_profiles}


def process_transaction(*args, **kwargs):
    """
    Retrieve a customer payment profile from the profile ID and return a tuple
    of the CIMResponse and a list of dictionaries containing data for each
    payment profile.

    See CreateTransactionRequest.__init__ for arguments and keyword arguments.
    """
    helper = CreateTransactionRequest(*args, **kwargs)
    response = helper.get_response()
    if response.transaction_response:
        if response.transaction_response.is_approved:
            payment_was_successful.send(sender=response.transaction_response)
        else:
            payment_was_flagged.send(sender=response.transaction_response)
    return response


class BaseRequest(object):
    """
    Abstract class used by all CIM request types
    """

    def __init__(self, action):
        self.create_base_document(action)
        if settings.AUTHNET_DEBUG:
            self.endpoint = AUTHNET_TEST_CIM_URL
        else:
            self.endpoint = AUTHNET_CIM_URL

    def create_base_document(self, action):
        """
        Create base document and root node and store them in self.document
        and self.root respectively.  The root node is created based on the
        action parameter.  The required merchant authentication node is added
        to the document automatically.
        """
        doc = xml.dom.minidom.Document()
        namespace = "AnetApi/xml/v1/schema/AnetApiSchema.xsd"
        root = doc.createElementNS(namespace, action)
        root.setAttribute("xmlns", namespace)
        doc.appendChild(root)

        self.document = doc
        authentication = doc.createElement("merchantAuthentication")
        name = self.get_text_node("name", settings.AUTHNET_LOGIN_ID)
        key = self.get_text_node("transactionKey",
                                 settings.AUTHNET_TRANSACTION_KEY)
        authentication.appendChild(name)
        authentication.appendChild(key)
        root.appendChild(authentication)

        self.root = root

    def get_response(self):
        """
        Submit request to Authorize.NET CIM server and return the resulting
        CIMResponse
        """
        request = urllib2.Request(self.endpoint,
                                  self.document.toxml().encode('utf-8'),
                                  {'Content-Type': 'text/xml'})
        raw_response = urllib2.urlopen(request)
        response_xml = xml.dom.minidom.parse(raw_response)
        self.process_response(response_xml)
        return self.create_response_object()

    def get_text_node(self, node_name, text):
        """
        Create a text-only XML node called node_name
        with contents of text
        """
        node = self.document.createElement(node_name)
        node.appendChild(self.document.createTextNode(unicode(text)))
        return node

    def create_response_object(self):
        return CIMResponse.objects.create(result=self.result,
                                          result_code=self.resultCode,
                                          result_text=self.resultText)

    def process_response(self, response):
        for e in response.childNodes[0].childNodes:
            if e.localName == 'messages':
                self.process_message_node(e)

    def process_message_node(self, node):
        for e in node.childNodes:
            if e.localName == 'resultCode':
                self.result = e.childNodes[0].nodeValue
            if e.localName == 'message':
                for f in e.childNodes:
                    if f.localName == 'code':
                        self.resultCode = f.childNodes[0].nodeValue
                    elif f.localName == 'text':
                        self.resultText = f.childNodes[0].nodeValue
 

class BasePaymentProfileRequest(BaseRequest):
    def get_payment_profile_node(self,
                                 billing_data,
                                 credit_card_data,
                                 node_name="paymentProfile"):
        payment_profile = self.document.createElement(node_name)

        if billing_data:
            bill_to = self.document.createElement("billTo")
            for key in BILLING_FIELDS:
                value = billing_data.get(key)
                if value is not None:
                    node = self.get_text_node(key, value)
                    bill_to.appendChild(node)
            payment_profile.appendChild(bill_to)

        payment = self.document.createElement("payment")
        credit_card = self.document.createElement("creditCard")
        for key in CREDIT_CARD_FIELDS:
            value = credit_card_data.get(key)
            if value is not None:
                node = self.get_text_node(key, value)
                credit_card.appendChild(node)
        payment.appendChild(credit_card)
        payment_profile.appendChild(payment)

        return payment_profile


class GetHostedProfilePageRequest(BaseRequest):
    """
    Request a token for retrieving a Hosted CIM form.

    Arguments (required):
    customer_profile_id -- the customer profile id

    Keyword Arguments (optional): Zero or more of:

    hostedProfileReturnUrl,
    hostedProfileReturnUrlText,
    hostedProfileHeadingBgColor,
    hostedProfilePageBorderVisible,
    hostedProfileIFrameCommunicatorUrl
    """
    def __init__(self, customer_profile_id, **settings):
        super(GetHostedProfilePageRequest,
              self).__init__('getHostedProfilePageRequest')
        self.root.appendChild(self.get_text_node('customerProfileId',
                                                 customer_profile_id))
        form_settings = self.document.createElement('hostedProfileSettings')
        for name, value in settings.iteritems():
            setting = self.document.createElement('setting')
            setting_name = self.get_text_node('settingName', name)
            setting_value = self.get_text_node('settingValue', value)
            setting.appendChild(setting_name)
            setting.appendChild(setting_value)
            form_settings.appendChild(setting)
        self.root.appendChild(form_settings)

    def process_response(self, response):
        self.profile_id = None
        self.payment_profile_id = None
        for e in response.childNodes[0].childNodes:
            if e.localName == 'messages':
                self.process_message_node(e)
            elif e.localName == 'token':
                self.token = e.childNodes[0].nodeValue


class BaseShippingProfileRequest(BaseRequest):
    def get_shipping_profile_node(self,
                                  shipping_data,
                                  node_name="shipToList"):
        shipping_profile = self.document.createElement(node_name)

        for key in SHIPPING_FIELDS:
            value = shipping_data.get(key)
            if value is not None:
                node = self.get_text_node(key, value)
                shipping_profile.appendChild(node)

        return shipping_profile


class CreateProfileRequest(BasePaymentProfileRequest,
                           BaseShippingProfileRequest):
    def __init__(self, customer_id=None, customer_email=None,
                 customer_description=None, billing_data=None,
                  shipping_data=None,credit_card_data=None):
        if not (customer_id or customer_email or customer_description):
            raise ValueError("%s requires one of 'customer_id', \
                             customer_email or customer_description"
                             % self.__class__.__name__)

        super(CreateProfileRequest,
              self).__init__("createCustomerProfileRequest")
        # order is important here, and OrderedDict not available < Python 2.7
        self.customer_info = SortedDict()
        self.customer_info['merchantCustomerId'] = customer_id
        self.customer_info['description'] = customer_description
        self.customer_info['email'] = customer_email
        profile_node = self.get_profile_node()
        if credit_card_data:
            payment_profiles = self.get_payment_profile_node(billing_data,
                                                             credit_card_data,
                                                             "paymentProfiles")
            profile_node.appendChild(payment_profiles)
        if shipping_data:
            shipping_profiles = self.get_shipping_profile_node(shipping_data,
                                                               "shipToList")
            profile_node.appendChild(shipping_profiles)
        self.root.appendChild(profile_node)

    def get_profile_node(self):
        profile = self.document.createElement("profile")
        for node_name, value in self.customer_info.items():
            if value:
                profile.appendChild(self.get_text_node(node_name, value))
        return profile

    def process_response(self, response):
        self.profile_id = None
        self.payment_profile_ids = None
        self.shipping_profile_ids = None
        for e in response.childNodes[0].childNodes:
            if e.localName == 'messages':
                self.process_message_node(e)
            elif e.localName == 'customerProfileId':
                self.profile_id = e.childNodes[0].nodeValue
            elif e.localName == 'customerPaymentProfileIdList':
                self.payment_profile_ids = []
                for f in e.childNodes:
                    self.payment_profile_ids.append(f.childNodes[0].nodeValue)
            elif e.localName == 'customerShippingAddressIdList':
                self.shipping_profile_ids = []
                for f in e.childNodes:
                    self.shipping_profile_ids.append(f.childNodes[0].nodeValue)


class DeleteProfileRequest(BaseRequest):
    """
    Deletes a Customer Profile

    Arguments:
    profile_id: The gateway-assigned customer ID.
    """
    def __init__(self, profile_id):
        super(DeleteProfileRequest,
              self).__init__("deleteCustomerProfileRequest")
        self.root.appendChild(self.get_text_node('customerProfileId',
                                                 profile_id))


class UpdatePaymentProfileRequest(BasePaymentProfileRequest):
    def __init__(self,
                 profile_id,
                 payment_profile_id,
                 billing_data=None,
                 credit_card_data=None):
        super(UpdatePaymentProfileRequest,
                self).__init__("updateCustomerPaymentProfileRequest")
        profile_id_node = self.get_text_node("customerProfileId", profile_id)
        payment_profile = self.get_payment_profile_node(billing_data,
                                                        credit_card_data,
                                                        "paymentProfile")
        payment_profile.appendChild(
                self.get_text_node("customerPaymentProfileId",
                                   payment_profile_id))
        self.root.appendChild(profile_id_node)
        self.root.appendChild(payment_profile)


class CreatePaymentProfileRequest(BasePaymentProfileRequest):
    def __init__(self, profile_id, billing_data=None, credit_card_data=None):
        super(CreatePaymentProfileRequest,
                self).__init__("createCustomerPaymentProfileRequest")
        profile_id_node = self.get_text_node("customerProfileId", profile_id)
        payment_profile = self.get_payment_profile_node(billing_data,
                                                        credit_card_data,
                                                        "paymentProfile")
        self.root.appendChild(profile_id_node)
        self.root.appendChild(payment_profile)

    def process_response(self, response):
        for e in response.childNodes[0].childNodes:
            if e.localName == 'messages':
                self.process_message_node(e)
            elif e.localName == 'customerPaymentProfileId':
                self.payment_profile_id = e.childNodes[0].nodeValue


class DeletePaymentProfileRequest(BasePaymentProfileRequest):
    def __init__(self, profile_id, payment_profile_id):
        super(DeletePaymentProfileRequest,
                self).__init__("deleteCustomerPaymentProfileRequest")
        profile_id_node = self.get_text_node("customerProfileId", profile_id)
        payment_profile_id_node = self.get_text_node(
                "customerPaymentProfileId",
                payment_profile_id)
        self.root.appendChild(profile_id_node)
        self.root.appendChild(payment_profile_id_node)


class UpdateShippingProfileRequest(BaseShippingProfileRequest):
    def __init__(self,
                 profile_id,
                 shipping_profile_id,
                 shipping_data=None,
                 credit_card_data=None):
        super(UpdateShippingProfileRequest,
                self).__init__("updateCustomerShippingAddressRequest")
        profile_id_node = self.get_text_node("customerProfileId", profile_id)
        shipping_profile = self.get_shipping_profile_node(shipping_data,
                                                          "address")
        shipping_profile.appendChild(
                self.get_text_node("customerAddressId",
                                   shipping_profile_id))
        self.root.appendChild(profile_id_node)
        self.root.appendChild(shipping_profile)


class CreateShippingProfileRequest(BaseShippingProfileRequest):
    def __init__(self, profile_id, shipping_data=None, credit_card_data=None):
        super(CreateShippingProfileRequest,
                self).__init__("createCustomerShippingAddressRequest")
        profile_id_node = self.get_text_node("customerProfileId", profile_id)
        shipping_profile = self.get_shipping_profile_node(shipping_data,
                                                          "address")
        self.root.appendChild(profile_id_node)
        self.root.appendChild(shipping_profile)

    def process_response(self, response):
        for e in response.childNodes[0].childNodes:
            if e.localName == 'messages':
                self.process_message_node(e)
            elif e.localName == 'customerAddressId':
                self.shipping_profile_id = e.childNodes[0].nodeValue


class DeleteShippingProfileRequest(BaseShippingProfileRequest):
    def __init__(self, profile_id, shipping_profile_id):
        super(DeleteShippingProfileRequest,
                self).__init__("deleteCustomerShippingAddressRequest")
        profile_id_node = self.get_text_node("customerProfileId", profile_id)
        shipping_profile_id_node = self.get_text_node(
                "customerAddressId",
                shipping_profile_id)
        self.root.appendChild(profile_id_node)
        self.root.appendChild(shipping_profile_id_node)


class GetProfileRequest(BaseRequest):
    def __init__(self, profile_id):
        super(GetProfileRequest, self).__init__("getCustomerProfileRequest")
        profile_id_node = self.get_text_node("customerProfileId", profile_id)
        self.root.appendChild(profile_id_node)

    def process_children(self, node, field_list):
        child_dict = {}
        for e in node.childNodes:
            if e.localName in field_list:
                if e.childNodes:
                    child_dict[e.localName] = e.childNodes[0].nodeValue
                else:
                    child_dict[e.localName] = ""
        return child_dict

    def extract_billing_data(self, node):
        return create_form_data(self.process_children(node, BILLING_FIELDS))

    def extract_credit_card_data(self, node):
        return create_form_data(
                self.process_children(node,
                CREDIT_CARD_FIELDS))

    def extract_payment_profiles_data(self, node):
        data = {}
        for e in node.childNodes:
            if e.localName == 'billTo':
                data['billing'] = self.extract_billing_data(e)
            if e.localName == 'payment':
                data['credit_card'] = self.extract_credit_card_data(
                        e.childNodes[0])
            if e.localName == 'customerPaymentProfileId':
                data['payment_profile_id'] = e.childNodes[0].nodeValue
        return data

    def extract_shipping_profiles_data(self, node):
        data = {}
        data['shipping'] = create_form_data(self.process_children(node, SHIPPING_FIELDS))
        for e in node.childNodes:
            if e.localName == 'customerAddressId':
                data['shipping_profile_id'] = e.childNodes[0].nodeValue
        return data

    def process_response(self, response):
        self.payment_profiles = []
        self.shipping_profiles = []
        for e in response.childNodes[0].childNodes:
            if e.localName == 'messages':
                self.process_message_node(e)
            if e.localName == 'profile':
                for f in e.childNodes:
                    if f.localName == 'paymentProfiles':
                        self.payment_profiles.append(
                                self.extract_payment_profiles_data(f))
                    elif f.localName == 'shipToList':
                        self.shipping_profiles.append(
                                self.extract_shipping_profiles_data(f))


class CreateTransactionRequest(BaseRequest):
    def __init__(self,
                 profile_id,
                 payment_profile_id,
                 transaction_type,
                 amount=None,
                 shipping_profile_id=None,
                 transaction_id=None,
                 card_code=None,
                 delimiter=None,
                 order_info=None):
        """
        Arguments:
        profile_id -- unique gateway-assigned profile identifier
        payment_profile_id -- unique gateway-assigned payment profile
                              identifier
        shipping_profile_id -- unique gateway-assigned shipping profile
                              identifier
        transaction_type -- One of the transaction types listed below.
        amount -- Dollar amount of transaction

        Keyword Arguments:
        transaction_id -- Required by PriorAuthCapture, Refund,
                          and Void transactions
        card_code -- The customer's card code (the three or four digit 
                          number on the back or front of a credit card)
        delimiter -- Delimiter used for transaction response data
        order_info -- a dict with optional order parameters `invoice_number`,
                      `description`, and `purchase_order_number` as keys.

        Accepted transaction types:
        AuthOnly, AuthCapture, CaptureOnly, PriorAuthCapture, Refund, Void
        """
        super(CreateTransactionRequest, self).__init__(
                "createCustomerProfileTransactionRequest")
        self.profile_id = profile_id
        self.payment_profile_id = payment_profile_id
        self.shipping_profile_id = shipping_profile_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.transaction_id = transaction_id
        self.card_code = card_code
        if delimiter:
            self.delimiter = delimiter
        else:
            self.delimiter = getattr(settings, 'AUTHNET_DELIM_CHAR', "|")
        self.add_transaction_node()
        self.add_extra_options()
        if order_info:
            self.add_order_info(**order_info)
        if self.card_code:
            card_code_node = self.get_text_node("cardCode", self.card_code)
            self.type_node.appendChild(card_code_node)

    def add_transaction_node(self):
        transaction_node = self.document.createElement("transaction")
        type_node = self.document.createElement("profileTrans%s" %
                self.transaction_type)

        if self.amount and self.transaction_type != "Void":
            amount_node = self.get_text_node("amount", self.amount)
            type_node.appendChild(amount_node)
        transaction_node.appendChild(type_node)
        self.add_profile_ids(type_node)
        if self.transaction_id:
            trans_id_node = self.get_text_node("transId", self.transaction_id)
            type_node.appendChild(trans_id_node)
        self.root.appendChild(transaction_node)
        self.type_node = type_node

    def add_profile_ids(self, transaction_type_node):
        profile_node = self.get_text_node("customerProfileId", self.profile_id)
        transaction_type_node.appendChild(profile_node)

        payment_profile_node = self.get_text_node("customerPaymentProfileId",
                                                  self.payment_profile_id)
        transaction_type_node.appendChild(payment_profile_node)
        if self.shipping_profile_id:
            shipping_profile_node = self.get_text_node(
                                                "customerShippingAddressId",
                                                self.shipping_profile_id)
            transaction_type_node.appendChild(shipping_profile_node)

    def add_order_info(self, invoice_number=None,
                       description=None,
                       purchase_order_number=None):
        if not (invoice_number or description or purchase_order_number):
            return
        order_node = self.document.createElement("order")
        if invoice_number:
            order_node.appendChild(self.get_text_node('invoiceNumber',
                                                      invoice_number))
        if description:
            order_node.appendChild(self.get_text_node('description',
                                                      description))
        if purchase_order_number:
            order_node.appendChild(self.get_text_node('purchaseOrderNumber',
                                                      purchase_order_number))
        self.type_node.appendChild(order_node)

    def add_extra_options(self):
        extra_options_node = self.get_text_node("extraOptions",
                "x_delim_data=TRUE&x_delim_char=%s" % self.delimiter)
        self.root.appendChild(extra_options_node)

    def create_response_object(self):
        try:
            response = Response.objects.create_from_list(
                    self.transaction_result)
        except AttributeError:
            response = None
        return CIMResponse.objects.create(result=self.result,
                                          result_code=self.resultCode,
                                          result_text=self.resultText,
                                          transaction_response=response)

    def process_response(self, response):
        for e in response.childNodes[0].childNodes:
            if e.localName == 'messages':
                self.process_message_node(e)
            if e.localName == 'directResponse':
                self.transaction_result = \
                        e.childNodes[0].nodeValue.split(self.delimiter)
