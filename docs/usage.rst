Usage
=====

Installation
------------

Install from `PyPI`_:

.. code-block:: bash

    $ pip install django-authorizenet

.. _PyPI: https://pypi.python.org/pypi/django-authorizenet/


Quickstart
----------

Add ``authorizenet`` to ``INSTALLED_APPS`` in your settings file:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'authorizenet',
    )

The following settings are required:

.. code-block:: python

    AUTHNET_DEBUG = True

    AUTHNET_LOGIN_ID = "yOuRl0g1nID"

    AUTHNET_TRANSACTION_KEY = "Tr4n5aCti0nK3y"
