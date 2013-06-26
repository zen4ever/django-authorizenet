from django.db import models


class CustomerProfileManager(models.Manager):

    def create(self, **data):

        """Create new Authorize.NET customer profile"""

        from .models import CustomerPaymentProfile

        kwargs = data
        sync = kwargs.pop('sync', True)
        kwargs = {
            'customer': kwargs.get('customer', None),
            'profile_id': kwargs.pop('profile_id', None),
        }

        # Create customer profile
        obj = self.model(**kwargs)
        self._for_write = True
        obj.save(force_insert=True, using=self.db, sync=sync, data=data)

        if sync:
            # Store customer payment profile data locally
            for payment_profile_id in obj.payment_profile_ids:
                CustomerPaymentProfile.objects.create(
                    customer_profile=obj,
                    payment_profile_id=payment_profile_id,
                    sync=False,
                    **data
                )

        return obj
