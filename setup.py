#!/usr/bin/env python

from distutils.core import setup
import os

setup(name='django-authorizenet',
      version='2.0',
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
)
