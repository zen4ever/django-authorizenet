from django.db import models

from authorizenet.cim import add_profile, create_payment_profile

from .exceptions import BillingError


class CustomerProfileManager(models.Manager):

    def create(self, **kwargs):

        """Create new Authorize.NET customer profile"""
        from .models import CustomerPaymentProfile

        user = kwargs.get('user')
        payment_data = kwargs.pop('payment_data', {})
        billing_data = kwargs.pop('billing_data', {})

        # Create the customer profile with Authorize.NET CIM call
        output = add_profile(user.pk, payment_data, billing_data)
        if not output['response'].success:
            raise BillingError("Error creating customer profile")
        kwargs['profile_id'] = output['profile_id']

        # Store customer profile data locally
        instance = super(CustomerProfileManager, self).create(**kwargs)

        # Store customer payment profile data locally
        for payment_profile_id in output['payment_profile_ids']:
            CustomerPaymentProfile.objects.create(
                customer_profile=instance,
                payment_profile_id=payment_profile_id,
                billing_data=billing_data,
                payment_data=payment_data,
                make_cim_request=False,
            )

        return instance


class CustomerPaymentProfileManager(models.Manager):

    def create(self, **kwargs):
        """Create new Authorize.NET customer payment profile"""
        customer_profile = kwargs.get('customer_profile')
        payment_data = kwargs.pop('payment_data', {})
        billing_data = kwargs.pop('billing_data', {})
        if kwargs.pop('make_cim_request', True):
            # Create the customer payment profile with Authorize.NET CIM call
            response, payment_profile_id = create_payment_profile(
                customer_profile.profile_id, payment_data, billing_data)
            if not response.success:
                raise BillingError()
            kwargs['payment_profile_id'] = payment_profile_id
        kwargs.update(billing_data)
        kwargs.update(payment_data)
        kwargs.pop('expiration_date')
        kwargs.pop('card_code')
        if 'card_number' in kwargs:
            kwargs['card_number'] = "XXXX%s" % kwargs['card_number'][-4:]
        return super(CustomerPaymentProfileManager, self).create(**kwargs)
