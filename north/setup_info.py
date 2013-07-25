"""
:copyright: Copyright 2013 by Luc Saffre.
:license: BSD, see LICENSE for more details.
"""

SETUP_INFO = dict(
  name = 'North',
  version = '0.1.5',
  install_requires = ['djangosite','Babel'],
  test_suite = 'tests',
  description = "Another way to migrate Django databases",
  #~ long_description=open('README.txt').read(),
  long_description="""\
North is a Python code serializer/deserializer for Django which lets 
you write intelligent fixtures and generate database dumps. 
You can use it to provide automated database migrations, which makes 
it an alternative to `South <http://south.aeracode.org/>`__

North includes an optional single-table solution for handling multilingual 
database content.

North doesn't require any database model, it is not even a Django app. 
Basic usage in your `settings.py` file is::

  from north import Site
  SITE = Site(__file__,globals(),'myapp1','myapp2',...)
  # your settings here
      
See the `Usage <http://site.lino-framework.org/usage.html>`_ page
for `djangosite` which applies entirely for a `North` site.

North works by adding a new serialization format "py" 
to Django's `SERIALIZATION_MODULES` setting.
You can then specify this in the `--format` option of 
Django's `dump` command::

  manage.py dump --format py

Instantiating a North Site will install sensible default values 
for certain Django settings, including `INSTALLED_APPS` and 
`SERIALIZATION_MODULES`.
""",
  license = 'Free BSD',
  packages = ['north','north.demo'],
  author = 'Luc Saffre',
  author_email = 'luc.saffre@gmail.com',
  url = "http://north.lino-framework.org",
  classifiers="""\
  Programming Language :: Python
  Programming Language :: Python :: 2.6
  Programming Language :: Python :: 2.7
  Development Status :: 4 - Beta
  Environment :: Web Environment
  Framework :: Django
  Intended Audience :: Developers
  Intended Audience :: System Administrators
  License :: OSI Approved :: BSD License
  Natural Language :: English
  Operating System :: OS Independent
  Topic :: Database :: Front-Ends
  Topic :: Software Development :: Libraries :: Application Frameworks""".splitlines())


