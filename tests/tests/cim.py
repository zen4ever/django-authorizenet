from copy import deepcopy
from datetime import datetime
from django.test import TestCase
from xml.dom.minidom import parseString
from httmock import HTTMock

from authorizenet.cim import extract_form_data, extract_payment_form_data, \
    add_profile

from .utils import xml_to_dict
from .mocks import cim_url_match, customer_profile_success
from .test_data import create_profile_success


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
            'card_number': "5586086832001747",
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
        self.request_data = deepcopy(create_profile_success)
        profile = self.request_data['createCustomerProfileRequest']['profile']
        del profile['paymentProfiles']['billTo']['phoneNumber']
        del profile['paymentProfiles']['billTo']['faxNumber']

    def test_add_profile_minimal(self):
        """Success test with minimal complexity"""
        @cim_url_match
        def request_handler(url, request):
            request_xml = parseString(request.body)
            self.assertEqual(xml_to_dict(request_xml), self.request_data)
            return customer_profile_success.format('createCustomerProfileResponse')
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
