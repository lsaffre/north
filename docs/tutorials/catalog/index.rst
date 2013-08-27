.. _mldbc_tutorial:

======================
Multilingual databases
======================

This tutorial shows how North supports
:ref:`multilingual database content <mldbc>`.

Let's create a little Site with the following 
:xfile:`models.py` file:

.. literalinclude:: models.py

..
  >>> from tutorials.catalog.models import *
  

The :xfile:`settings.py` file is where you specify the 
:attr:`languages <north.Site.languages>` 
setting of a given Site instance:

.. literalinclude:: settings.py
  

The `demo` fixture
------------------

Now we install some demo data. Here is a :ref:`Python fixture <dpy>`:

.. literalinclude:: fixtures/demo.py

Note how the application developer doesn't know which 
:attr:`languages <north.Site.languages>` setting at runtime.

Of course the fixture above supposes a single person who knows 
all the languages, but that's just because we are simplifying. 
In reality you can do it as sophisticated as you want, 
reading the content from different sources.

Here is how to install this data:

>>> from django.core.management import call_command
>>> call_command('initdb','demo',interactive=False)
Creating tables ...
Creating table catalog_product
Installing custom SQL ...
Installing indexes ...
Installed 6 object(s) from 1 fixture(s)

And finally we can print a catalog in different languages:

>>> print ', '.join([unicode(p) for p in Product.objects.all()])
Chair, Table, Monitor, Mouse, Keyboard, Consultation

>>> from north.dbutils import set_language
>>> set_language('de')
>>> print ', '.join([unicode(p) for p in Product.objects.all()])
Stuhl, Tisch, Bildschirm, Maus, Tastatur, Beratung

North doesn't impose any templating or other system to do 
that, so the formatting details are not subject of this tutorial.

Formatting dates
----------------

The :func:`north.dbutils.format_date` function is a thin wrapper 
to the corresponding function in `babel.dates`, 
filling the `locale` parameter according to Django's 
current language (and doing the conversion).

The major advantage over using `date_format` from `django.utils.formats` 
is that Babel offers a "full" format:

>>> import datetime
>>> today = datetime.date(2013,01,18)
>>> from north.dbutils import format_date

>>> set_language(None)
>>> print format_date(today,'full')
Friday, January 18, 2013

>>> set_language('fr')
>>> print format_date(today,'full')
vendredi 18 janvier 2013

>>> set_language('de')
>>> print format_date(today,'full')
Freitag, 18. Januar 2013

You can use this also for languages that aren't on your site:

>>> set_language('et')
>>> print format_date(today,'full')
reede, 18. jaanuar 2013

>>> set_language('nl')
>>> print format_date(today,'full')
vrijdag 18 januari 2013



Where to go next
----------------

One detail is missing to make North's multi-lingual fields 
usable in a normal Django project: a possibility to integrate 
these variable fields into your Admin form.

I didn't write this until now because nobody asked me, and 
because Lino has built-in support for North's BabelFields.
See also :ref:`lino:mldbc_tutorial`

