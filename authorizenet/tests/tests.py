from datetime import datetime
from django.test import TestCase
from xml.dom.minidom import parseString
from httmock import urlmatch, HTTMock

from authorizenet.cim import extract_form_data, extract_payment_form_data, \
    add_profile


cim_url_match = urlmatch(scheme='https', netloc=r'^api\.authorize\.net$',
                         path=r'^/xml/v1/request\.api$')


success_response = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<{0}>'
    '<messages>'
    '<resultCode>Ok</resultCode>'
    '<message><code>I00001</code><text>Successful.</text></message>'
    '</messages>'
    '<customerProfileId>6666</customerProfileId>'
    '<customerPaymentProfileIdList>'
    '<numericString>7777</numericString>'
    '</customerPaymentProfileIdList>'
    '<customerShippingAddressIdList />'
    '<validationDirectResponseList />'
    '</{0}>'
)


def xml_to_dict(node):
    node_data = {}
    if node.nodeType == node.TEXT_NODE:
        node_data = node.data
    elif node.nodeType not in (node.DOCUMENT_NODE, node.DOCUMENT_TYPE_NODE):
        node_data.update(node.attributes.items())
    if node.nodeType not in (node.TEXT_NODE, node.DOCUMENT_TYPE_NODE):
        for child in node.childNodes:
            child_name, child_data = xml_to_dict(child)
            if not child_data:
                child_data = ''
            if child_name not in node_data:
                node_data[child_name] = child_data
            else:
                if not isinstance(node_data[child_name], list):
                    node_data[child_name] = [node_data[child_name]]
                node_data[child_name].append(child_data)
        if node_data.keys() == ['#text']:
            node_data = node_data['#text']
    if node.nodeType == node.DOCUMENT_NODE:
        return node_data
    else:
        return node.nodeName, node_data


class ExtractFormDataTests(TestCase):

    """Tests for utility functions converting form data to CIM data"""

    def test_extract_form_data(self):
        new_data = extract_form_data({'word': "1", 'multi_word_str': "2"})
        self.assertEqual(new_data, {'word': "1", 'multiWordStr': "2"})

    def test_extract_payment_form_data(self):
        data = extract_payment_form_data({
            'card_number': "1111",
            'expiration_date': datetime(2020, 5, 1),
            'card_code': "123",
        })
        self.assertEqual(data, {
            'cardNumber': "1111",
            'expirationDate': "2020-05",
            'cardCode': "123",
        })


class AddProfileTests(TestCase):

    """Tests for add_profile utility function"""

    def setUp(self):
        self.payment_form_data = {
            'card_number': "1111222233334444",
            'expiration_date': datetime(2020, 5, 1),
            'card_code': "123",
        }
        self.billing_form_data = {
            'first_name': "Danielle",
            'last_name': "Thompson",
            'company': "",
            'address': "101 Broadway Avenue",
            'city': "San Diego",
            'state': "CA",
            'country': "US",
            'zip': "92101",
        }
        self.request_data = {
            'createCustomerProfileRequest': {
                'xmlns': 'AnetApi/xml/v1/schema/AnetApiSchema.xsd',
                'profile': {
                    'merchantCustomerId': '42',
                    'paymentProfiles': {
                        'billTo': {
                            'firstName': 'Danielle',
                            'lastName': 'Thompson',
                            'company': '',
                            'address': '101 Broadway Avenue',
                            'city': 'San Diego',
                            'state': 'CA',
                            'zip': '92101',
                            'country': 'US'
                        },
                        'payment': {
                            'creditCard': {
                                'cardCode': '123',
                                'cardNumber': '1111222233334444',
                                'expirationDate': '2020-05'
                            }
                        }
                    }
                },
                'merchantAuthentication': {
                    'transactionKey': 'key',
                    'name': 'loginid'
                },
            }
        }

    def test_add_profile_minimal(self):
        """Success test with minimal complexity"""
        @cim_url_match
        def request_handler(url, request):
            request_xml = parseString(request.body)
            self.assertEqual(xml_to_dict(request_xml), self.request_data)
            return success_response.format('createCustomerProfileResponse')
        with HTTMock(request_handler):
            result = add_profile(42, self.payment_form_data,
                                 self.billing_form_data)
            response = result.pop('response')
            self.assertEqual(result, {
                'profile_id': '6666',
                'payment_profile_ids': ['7777'],
                'shipping_profile_ids': [],
            })
            self.assertEqual(response.result, 'Ok')
            self.assertEqual(response.result_code, 'I00001')
            self.assertEqual(response.result_text, 'Successful.')
            self.assertIsNone(response.transaction_response)
