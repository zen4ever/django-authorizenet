#!/usr/bin/env python

from setuptools import setup, find_packages
import os

setup(name='django-authorizenet',
      version='2.1',
      description='Django and Authorize.NET payment gateway integration',
      author='Andrii Kurinnyi',
      author_email='andrew@zen4ever.com',
      url='http://github.com/zen4ever/django-authorizenet/tree/master',
      packages=['authorizenet', 'authorizenet.migrations'],
      keywords=['django', 'Authorize.NET', 'payment'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Programming Language :: Python',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Framework :: Django',
          'Topic :: Office/Business :: Financial',
      ],
      long_description=open(
          os.path.join(os.path.dirname(__file__), 'README.rst'),
      ).read().strip(),
      test_suite='runtests.runtests',
      tests_require=['httmock'],
      install_requires=['requests', 'django>=1.4.2',
                        'django-relatives>=0.3.1'])
