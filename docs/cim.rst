CIM Usage
=========

The easiest way to use the CIM support is to use the ``CustomerProfile`` and
``CustomerPaymentProfile`` models provided by the ``authorizenet`` app.  These
models map the ORM CRUD operations to Authorize.NET calls, making it easy to
keep your local and remote data in sync.

Customer profiles contain a one-to-one field ``customer`` which links to the
Django user model by default.  This foreign key target may be customized in the
``CUSTOMER_MODEL`` setting in your settings module.

Using built-in models
---------------------

CustomerPaymentProfile Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When the ``save()`` method is called on a ``CustomerPaymentProfile`` instance,
the payment profile is created or update on Authorize.NET and saved to the
database.  A ``CustomerProfile`` will also be created if the specified
``customer`` doesn't have one yet.

When the ``delete()`` method is called on a ``CustomerPaymentProfile``
instance, the payment profile is deleted on Authorize.NET and deleted from the
database.

Payment Profile Form
~~~~~~~~~~~~~~~~~~~~

The ``CustomerPaymentForm`` available in ``authorizenet.forms`` allows a
``CustomerPaymentProfile`` to be easily created or updated for a given
``customer``.  This form is just a model form for the
``CustomerPaymentProfile`` model.

Generic Views
~~~~~~~~~~~~~

The ``PaymentProfileCreateView`` and ``PaymentProfileUpdateView`` allow
``CustomerPaymentProfile`` instances can be created and updated with ease.
The ``customer`` argument sent to ``CustomerPaymentForm`` defaults to the
currently authenticated user.
