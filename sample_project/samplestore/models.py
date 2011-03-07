from django.db import models
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField, USStateField
from django.db.models.signals import post_save


ADDRESS_CHOICES = (
     ('billing', 'Billing'),
     ('shipping', 'Shipping'),
)


class Customer(models.Model):
    user = models.ForeignKey(User)
    shipping_same_as_billing = models.BooleanField(default=True)

    def __unicode__(self):
        return self.user.username


class Address(models.Model):
    type = models.CharField(max_length=10, choices=ADDRESS_CHOICES)
    customer = models.ForeignKey(Customer)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=60)
    city = models.CharField(max_length=40)
    state = USStateField()
    zip_code = models.CharField(max_length=20)
    phone = PhoneNumberField(blank=True)
    fax = PhoneNumberField(blank=True)

    def __unicode__(self):
        return self.customer.user.username


class Item(models.Model):
    title = models.CharField(max_length=55)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __unicode__(self):
        return self.title


class Invoice(models.Model):
    customer = models.ForeignKey(Customer)
    item = models.ForeignKey(Item)

    def __unicode__(self):
        return u"<Invoice: %d - %s>" % (self.id, self.customer.user.username)


def create_customer_profile(sender, instance=None, **kwargs):
    if instance is None:
        return
    profile, created = Customer.objects.get_or_create(user=instance)


post_save.connect(create_customer_profile, sender=User)
