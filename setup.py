#!/usr/bin/env python

from distutils.core import setup

setup(name='django-ajaxerrors',
      version='1.0',
      description='Django middleware for unhandled AJAX errors',
      author='Yaniv Aknin',
      author_email='yaniv+django.ajaxerrors@aknin.name',
      url='https://github.com/yaniv-aknin/django-ajaxerrors',
      packages=['ajaxerrors'],
      license='MIT',
     )
