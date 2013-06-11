from datetime import datetime
from django.test import TestCase, LiveServerTestCase
from xml.dom.minidom import parseString
from httmock import HTTMock

from authorizenet.cim import extract_form_data, extract_payment_form_data, \
    add_profile
from authorizenet.models import CustomerProfile, CustomerPaymentProfile

from .utils import create_user, xml_to_dict
from .mocks import cim_url_match, success_response
from .test_data import create_profile_success, update_profile_success


class PaymentProfileCreationTests(LiveServerTestCase):

    def setUp(self):
        self.user = create_user(id=42, username='billy', password='password')
        self.client.login(username='billy', password='password')

    def test_create_new_customer_get(self):
        response = self.client.get('/customers/create')
        self.assertNotIn("This field is required", response.content)
        self.assertIn("Credit Card Number", response.content)
        self.assertIn("City", response.content)

    def test_create_new_customer_post_error(self):
        response = self.client.post('/customers/create')
        self.assertIn("This field is required", response.content)
        self.assertIn("Credit Card Number", response.content)
        self.assertIn("City", response.content)

    def test_create_new_customer_post_success(self):
        @cim_url_match
        def create_customer_success(url, request):
            request_xml = parseString(request.body)
            self.assertEqual(xml_to_dict(request_xml),
                             create_profile_success)
            return success_response.format('createCustomerProfileResponse')
        self.maxDiff = None
        with HTTMock(create_customer_success):
            response = self.client.post('/customers/create', {
                'card_number': "5586086832001747",
                'expiration_date_0': "5",
                'expiration_date_1': "2020",
                'card_code': "123",
                'first_name': "Danielle",
                'last_name': "Thompson",
                'address': "101 Broadway Avenue",
                'city': "San Diego",
                'state': "CA",
                'country': "US",
                'zip': "92101",
            }, follow=True)
        self.assertIn("success", response.content)


class PaymentProfileUpdateTests(LiveServerTestCase):

    def setUp(self):
        self.user = create_user(id=42, username='billy', password='password')
        profile = CustomerProfile(user=self.user, profile_id='6666')
        profile.save()
        self.payment_profile = CustomerPaymentProfile(
            customer_profile=profile,
            payment_profile_id='7777',
        )
        self.payment_profile.save()
        self.client.login(username='billy', password='password')

    def test_update_profile_get(self):
        response = self.client.get('/customers/update')
        self.assertNotIn("This field is required", response.content)
        self.assertIn("Credit Card Number", response.content)
        self.assertIn("City", response.content)

    def test_update_profile_post_error(self):
        response = self.client.post('/customers/update')
        self.assertIn("This field is required", response.content)
        self.assertIn("Credit Card Number", response.content)
        self.assertIn("City", response.content)

    def test_update_profile_post_success(self):
        @cim_url_match
        def create_customer_success(url, request):
            request_xml = parseString(request.body)
            self.assertEqual(xml_to_dict(request_xml),
                             update_profile_success)
            return success_response.format('updateCustomerProfileResponse')
        self.maxDiff = None
        with HTTMock(create_customer_success):
            response = self.client.post('/customers/update', {
                'card_number': "5586086832001747",
                'expiration_date_0': "5",
                'expiration_date_1': "2020",
                'card_code': "123",
                'first_name': "Danielle",
                'last_name': "Thompson",
                'address': "101 Broadway Avenue",
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
        self.request_data = create_profile_success

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
