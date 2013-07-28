from datetime import date
from django.test import LiveServerTestCase
from xml.dom.minidom import parseString
from httmock import HTTMock

from authorizenet.models import CustomerProfile, CustomerPaymentProfile

from .utils import create_user, xml_to_dict
from .mocks import cim_url_match, customer_profile_success, \
    payment_profile_success
from .test_data import create_profile_success, update_profile_success, \
    create_payment_profile_success


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
            self.assertEqual(xml_to_dict(request_xml), create_profile_success)
            return customer_profile_success.format('createCustomerProfileResponse')
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

    def test_create_new_payment_profile_post_success(self):
        @cim_url_match
        def request_handler(url, request):
            request_xml = parseString(request.body)
            self.assertEqual(xml_to_dict(request_xml),
                             create_payment_profile_success)
            return payment_profile_success.format('createCustomerPaymentProfileResponse')
        CustomerProfile.objects.create(customer=self.user, profile_id='6666', sync=False)
        with HTTMock(request_handler):
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
        profile = CustomerProfile(customer=self.user, profile_id='6666')
        profile.save(sync=False)
        self.payment_profile = CustomerPaymentProfile(
            customer=self.user,
            customer_profile=profile,
            payment_profile_id='7777',
        )
        self.payment_profile.save(sync=False)
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
            return customer_profile_success.format('updateCustomerProfileResponse')
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
        payment_profile = self.user.customer_profile.payment_profiles.get()
        self.assertEqual(payment_profile.raw_data, {
            'id': payment_profile.id,
            'customer_profile': self.user.customer_profile.id,
            'customer': self.user.id,
            'payment_profile_id': '7777',
            'card_number': 'XXXX1747',
            'expiration_date': date(2020, 5, 31),
            'card_code': None,
            'first_name': 'Danielle',
            'last_name': 'Thompson',
            'company': '',
            'fax_number': '',
            'phone_number': '',
            'address': '101 Broadway Avenue',
            'city': 'San Diego',
            'state': 'CA',
            'country': 'US',
            'zip': '92101',
        })

