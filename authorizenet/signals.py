from django.dispatch import Signal

__all__ = ['payment_was_successful',
           'payment_was_flagged',
           'customer_was_created',
           'customer_was_flagged']

payment_was_successful = Signal()
payment_was_flagged = Signal()

customer_was_created = Signal(["customer_id",
                               "customer_description",
                               "customer_email",
                               "profile_id",
                               "payment_profile_ids"])
customer_was_flagged = Signal(["customer_id", "customer_description", "customer_email"])
