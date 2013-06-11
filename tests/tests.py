from datetime import datetime
from django.test import TestCase, LiveServerTestCase
from xml.dom.minidom import parseString
from httmock import HTTMock

from authorizenet.cim import extract_form_data, extract_payment_form_data, \
    add_profile

from .utils import create_user, xml_to_dict
from .mocks import cim_url_match, success_response


class PaymentProfileCreationTests(LiveServerTestCase):

    def test_create_new_customer_get(self):
        create_user(username='billy', password='password')
        self.client.login(username='billy', password='password')
        response = self.client.get('/customers/create')
        self.assertNotIn("This field is required", response.content)
        self.assertIn("Credit Card Number", response.content)
        self.assertIn("City", response.content)

    def test_create_new_customer_post_error(self):
        create_user(username='billy', password='password')
        self.client.login(username='billy', password='password')
        response = self.client.post('/customers/create')
        self.assertIn("This field is required", response.content)
        self.assertIn("Credit Card Number", response.content)
        self.assertIn("City", response.content)

    def test_create_new_customer_post_success(self):
        create_user(username='billy', password='password')
        self.client.login(username='billy', password='password')
        response = self.client.post('/customers/create', {
            'card_number': "5586086832001747",
            'expiration_date_0': "4",
            'expiration_date_1': "2020",
            'card_code': "123",
            'first_name': "Billy",
            'last_name': "Monaco",
            'address': "101 Broadway Ave",
            'city': "San Diego",
            'state': "CA",
            'country': "US",
            'zip': "92101",
        }, follow=True)
        self.assertIn("success", response.content)


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
