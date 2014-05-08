.. _north.settings:

====================================
Settings reference
====================================

.. note:: This page is not maintained. Contents has been copied to Lino docs.

Here is a list of attributes and methods of a :ref:`north` `Site`
instance which application developers should know.
See also :ref:`djangosite.settings`.

.. setting:: migration_class

Used by :func:`north.dpy.install_migrations`.


.. setting:: languages

The language distribution used on this site.

This must be either `None` or an iterable of language codes.
Or a string containing a space-separated suite of language codes.

Examples::

  languages = "en de fr nl et".split()
  languages = ['en']
  languages = 'en fr'

See :meth:`apply_languages` for more detailed description.

The first language in this list will be the site's 
default language.

Changing this setting affects your database structure 
if your application uses babel fields,
and thus require a :ref:`data migration <datamig>`.

If this is not `None`, Site will set the Django settings 
`USE_L10N <http://docs.djangoproject.com/en/dev/ref/settings/#use-l10n>`_ 
and
`LANGUAGE_CODE <http://docs.djangoproject.com/en/dev/ref/settings/#language-code>`_.



>>> from django.utils import translation
>>> from north import TestSite as Site
>>> from pprint import pprint
>>> pprint(Site().django_settings) #doctest: +ELLIPSIS
{'DATABASES': {'default': {'ENGINE': 'django.db.backends.sqlite3',
                           'NAME': '...default.db'}},
 'FIXTURE_DIRS': (),
 'INSTALLED_APPS': ('north', 'djangosite'),
 'LANGUAGES': [],
 'LOCALE_PATHS': (),
 'SECRET_KEY': '20227',
 'SERIALIZATION_MODULES': {'py': 'north.dpy'},
 '__file__': '...'}

>>> pprint(Site(languages="en fr de").languages)
(LanguageInfo(django_code='en', name='en', index=0, suffix=''),
 LanguageInfo(django_code='fr', name='fr', index=1, suffix='_fr'),
 LanguageInfo(django_code='de', name='de', index=2, suffix='_de'))

>>> pprint(Site(languages="de-ch de-be").languages)
(LanguageInfo(django_code='de-ch', name=u'de_CH', index=0, suffix=''),
 LanguageInfo(django_code='de-be', name=u'de_BE', index=1, suffix='_de_BE'))

If we have more than languages en-us and en-gb *on a same Site*, 
then it is not allowed to specify just "en". 
But in most cases it is allowed to just say "en", which will 
mean "the English variant used on this Site".

>>> site = Site(languages="en-us fr de-be de")
>>> pprint(site.languages)
(LanguageInfo(django_code='en-us', name=u'en_US', index=0, suffix=''),
 LanguageInfo(django_code='fr', name='fr', index=1, suffix='_fr'),
 LanguageInfo(django_code='de-be', name=u'de_BE', index=2, suffix='_de_BE'),
 LanguageInfo(django_code='de', name='de', index=3, suffix='_de'))

>>> pprint(site.language_dict)
{'de': LanguageInfo(django_code='de', name='de', index=3, suffix='_de'),
 u'de_BE': LanguageInfo(django_code='de-be', name=u'de_BE', index=2, suffix='_de_BE'),
 'en': LanguageInfo(django_code='en-us', name=u'en_US', index=0, suffix=''),
 u'en_US': LanguageInfo(django_code='en-us', name=u'en_US', index=0, suffix=''),
 'fr': LanguageInfo(django_code='fr', name='fr', index=1, suffix='_fr')}

>>> site.startup()
>>> pprint(site.django_settings['LANGUAGES']) #doctest: +ELLIPSIS
[('de', 'German'), ('fr', 'French')]


.. setting:: field2kw

Method ``field2kw(obj,name,**known_values)``

Examples:

>>> from north import TestSite as Site
>>> from atelier.utils import AttrDict
>>> def testit(site_languages):
...     site = Site(languages=site_languages)
...     obj = AttrDict(site.babelkw('name',de="Hallo",en="Hello",fr="Salut"))
...     return site,obj


>>> site,obj = testit('de en')
>>> site.field2kw(obj,'name')
{'de': 'Hallo', 'en': 'Hello'}

>>> site,obj = testit('fr et')
>>> site.field2kw(obj,'name')
{'fr': 'Salut'}

        
.. setting:: babelitem

``babelitem(*args,**values)``

Given a dictionary with babel values, return the 
value corresponding to the current language.

This is available in templates as a function `tr`.

>>> kw = dict(de="Hallo",en="Hello",fr="Salut")

>>> from north import TestSite as Site
>>> from django.utils import translation

A Site with default language "de":

>>> site = Site(languages="de en")
>>> tr = site.babelitem
>>> with translation.override('de'):
...    tr(**kw)
'Hallo'

>>> with translation.override('en'):
...    tr(**kw)
'Hello'

If the current language is not found in the specified `values`,
then it returns the site's default language ("de" in our example):

>>> with translation.override('jp'):
...    tr(en="Hello",de="Hallo",fr="Salut")
'Hallo'

Another way is to specify an explicit default value using a
positional argument. In that case the language's default language
doesn'n matter:

>>> with translation.override('jp'):
...    tr("Hello",de="Hallo",fr="Salut")
'Hello'

>>> with translation.override('de'):
...     tr("Hello",de="Hallo",fr="Salut")
'Hallo'

You may not specify more than one default value:

>>> tr("Hello","Hallo")
Traceback (most recent call last):
...
ValueError: ('Hello', 'Hallo') is more than 1 default value.



.. setting:: hidden_languages

A string of django codes of languages that should be hidden.

Lino Welfare uses this because the demo database has 4 
languages, but `nl` is currently hidden bu default.


.. setting:: migration_module

If you maintain a data migration module for your application, 
specify its name here.
See :ref:`datamig`.



.. setting:: loading_from_dump

This is normally `False`, except when the process is loading data from
a Python dump.

The Python dump then calls :func:`north.dpy.install_migrations` which
sets this to `True`.

Application code should not change this setting (except for certain
special test cases).



