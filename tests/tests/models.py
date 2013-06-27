from httmock import HTTMock, with_httmock
from xml.dom.minidom import parseString
from django.test import TestCase
from authorizenet.models import CustomerProfile

from .utils import create_user, xml_to_dict
from .mocks import cim_url_match, customer_profile_success, delete_success
from .test_data import create_empty_profile_success, delete_profile_success


class RequestError(Exception):
    pass


def error_on_request(url, request):
    raise RequestError("CIM Request")


class CustomerProfileModelTests(TestCase):

    """Tests for CustomerProfile model"""

    def setUp(self):
        self.user = create_user(id=42, username='billy', password='password')

    def create_profile(self):
        return CustomerProfile.objects.create(
            customer=self.user, profile_id='6666', sync=False)

    def test_create_sync_no_data(self):
        @cim_url_match
        def request_handler(url, request):
            request_xml = parseString(request.body)
            self.assertEqual(xml_to_dict(request_xml),
                             create_empty_profile_success)
            return customer_profile_success.format(
                'createCustomerProfileResponse')
        profile = CustomerProfile(customer=self.user)
        with HTTMock(error_on_request):
            self.assertRaises(RequestError, profile.save)
        self.assertEqual(profile.profile_id, '')
        with HTTMock(request_handler):
            profile.save(sync=True)
        self.assertEqual(profile.profile_id, '6666')

    @with_httmock(error_on_request)
    def test_create_no_sync(self):
        profile = CustomerProfile(customer=self.user)
        profile.save(sync=False)
        self.assertEqual(profile.profile_id, '')

    @with_httmock(error_on_request)
    def test_edit(self):
        profile = self.create_profile()
        self.assertEqual(profile.profile_id, '6666')
        profile.profile_id = '7777'
        profile.save()
        self.assertEqual(profile.profile_id, '7777')
        profile.profile_id = '8888'
        profile.save(sync=True)
        self.assertEqual(profile.profile_id, '8888')
        profile.profile_id = '9999'
        profile.save(sync=False)
        self.assertEqual(profile.profile_id, '9999')

    def test_delete(self):
        @cim_url_match
        def request_handler(url, request):
            request_xml = parseString(request.body)
            self.assertEqual(xml_to_dict(request_xml),
                             delete_profile_success)
            return delete_success.format(
                'deleteCustomerProfileResponse')
        profile = self.create_profile()
        with HTTMock(request_handler):
            profile.delete()
        self.assertEqual(profile.__class__.objects.count(), 0)
