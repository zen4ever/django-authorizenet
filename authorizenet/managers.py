from django.db import models

from authorizenet.cim import add_profile

from .exceptions import BillingError


class CustomerProfileManager(models.Manager):

    def create(self, **data):

        """Create new Authorize.NET customer profile"""
        from .models import CustomerPaymentProfile

        kwargs = data
        sync = kwargs.pop('sync', True)
        kwargs = {
            'user': kwargs.pop('user', None),
            'profile_id': kwargs.pop('profile_id', None),
        }

        # Create the customer profile with Authorize.NET CIM call
        if sync:
            output = add_profile(kwargs['user'].pk, data, data)
            if not output['response'].success:
                raise BillingError("Error creating customer profile")
            kwargs['profile_id'] = output['profile_id']

        # Store customer profile data locally
        instance = super(CustomerProfileManager, self).create(**kwargs)

        if sync:
            # Store customer payment profile data locally
            for payment_profile_id in output['payment_profile_ids']:
                CustomerPaymentProfile.objects.create(
                    customer_profile=instance,
                    payment_profile_id=payment_profile_id,
                    sync=False,
                    **data
                )

        return instance


class CustomerPaymentProfileManager(models.Manager):

    def create(self, **kwargs):
        """Create new Authorize.NET customer payment profile"""
        sync = kwargs.pop('sync', True)
        obj = self.model(**kwargs)
        self._for_write = True
        obj.save(force_insert=True, using=self.db, sync=sync)
        return obj
