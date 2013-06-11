from django.test import LiveServerTestCase
from django.contrib.auth.models import User


def create_user(username='', password=''):
    user = User(username=username)
    user.set_password(password)
    user.save()
    return user


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
