import os
from setuptools import setup

execfile(os.path.join(os.path.dirname(__file__),'north','version.py'))

setup(name = 'django-north',
  version = __version__,
  description = """A Python code serializer/deserializer for Django which lets you write intelligent fixtures and generate database dumps. Optionally an alternative to South for managing database migrations. Includes an optional single-table solution for handling multilingual database content.""",
  license = 'Free BSD',
  packages = ['north'],
  author = 'Luc Saffre',
  author_email = 'luc.saffre@gmail.com',
  requires = ['Django','django_site'],
  url = "http://north.lino-framework.org",
  #~ test_suite = 'lino.test_apps',
  classifiers="""\
  Programming Language :: Python
  Programming Language :: Python :: 2
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
