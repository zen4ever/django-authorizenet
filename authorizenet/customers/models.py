from django.db import models

from authorizenet.cim import (get_profile, update_payment_profile,
                              delete_payment_profile)

from .managers import CustomerProfileManager, CustomerPaymentProfileManager
from .exceptions import BillingError


class CustomerProfile(models.Model):

    """Authorize.NET customer profile"""

    user = models.ForeignKey('auth.User', unique=True)
    profile_id = models.CharField(max_length=50)

    def sync(self):
        """Overwrite local customer profile data with remote data"""
        response, payment_profiles = get_profile(self.profile_id)
        if not response.success:
            raise BillingError("Error syncing remote customer profile")
        for payment_profile in payment_profiles:
            instance, created = CustomerPaymentProfile.objects.get_or_create(
                customer_profile=self,
                payment_profile_id=payment_profile['payment_profile_id']
            )
            instance.sync(payment_profile)

    objects = CustomerProfileManager()


class CustomerPaymentProfile(models.Model):

    """Authorize.NET customer payment profile"""

    customer_profile = models.ForeignKey('CustomerProfile',
                                         related_name='payment_profiles')
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    company = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=60, blank=True)
    city = models.CharField(max_length=40, blank=True)
    state = models.CharField(max_length=40, blank=True)
    zip = models.CharField(max_length=20, blank=True, verbose_name="ZIP")
    country = models.CharField(max_length=60, blank=True)
    phone = models.CharField(max_length=25, blank=True)
    fax = models.CharField(max_length=25, blank=True)
    payment_profile_id = models.CharField(max_length=50)
    card_number = models.CharField(max_length=16, blank=True)

    def raw_data(self):
        """Return data suitable for use in payment and billing forms"""
        return model_to_dict(self)

    def sync(self, data):
        """Overwrite local customer payment profile data with remote data"""
        for k, v in data.get('billing', {}).items():
            setattr(self, k, v)
        self.card_number = data.get('credit_card', {}).get('card_number',
                                                           self.card_number)
        self.save()

    def delete(self):
        """Delete the customer payment profile remotely and locally"""
        delete_payment_profile(self.customer_profile.profile_id,
                               self.payment_profile_id)

    def update(self, payment_data, billing_data):
        """Update the customer payment profile remotely and locally"""
        response = update_payment_profile(self.customer_profile.profile_id,
                                          self.payment_profile_id,
                                          payment_data, billing_data)
        if not response.success:
            raise BillingError()
        for k, v in billing_data.items():
            setattr(self, k, v)
        for k, v in payment_data.items():
            # Do not store expiration date and mask credit card number
            if k != 'expiration_date' and k != 'card_code':
                if k == 'card_number':
                    v = "XXXX%s" % v[-4:]
                setattr(self, k, v)
        self.save()

    def __unicode__(self):
        return self.card_number

    objects = CustomerPaymentProfileManager()
