.. _mldbc_tutorial:

======================
Multilingual databases
======================

This tutorial shows how North supports
:ref:`multilingual database content <mldbc>`.

Let's create a little Site with the following 
:xfile:`models.py` file:

.. literalinclude:: catalog/models.py

And here is the :xfile:`settings.py` file:

.. literalinclude:: catalog/settings.py

This is where you specify the 
:attr:`languages <north.Site.languages>` 
setting of a given Site instance.


.. djangodoctest:: tutorials.catalog.settings

Now we install some demo data:

>>> # -*- coding: utf-8 -*-
>>> from django.conf import settings
>>> settings.SITE.call_command('initdb','demo',interactive=False)
Creating tables ...
Creating table catalog_product
Installing custom SQL ...
Installing indexes ...
Installed 6 object(s) from 1 fixture(s)

And finally we can print a catalog in different languages:

>>> from tutorials.catalog.models import Product
>>> print ', '.join([unicode(p) for p in Product.objects.all()])
Chair, Table, Monitor, Mouse, Keyboard, Consultation

>>> from north.babel import set_language
>>> set_language('de')
>>> print ', '.join([unicode(p) for p in Product.objects.all()])
Stuhl, Tisch, Bildschirm, Maus, Tastatur, Beratung


North doesn't impose any templating or other system to do 
that, so the formatting details are not subject of this tutorial.


The `demo` fixture
------------------

.. literalinclude:: catalog/fixtures/demo.py

Note how the application developer doesn't know which 
:attr:`languages <north.Site.languages>` setting at runtime.

Of course the fixture above supposes a single person who knows 
all the languages, but that's just because we are simplifying. 
In reality you can do it as sophisticated as you want, 
reading the content from different sources.

Where to go next
----------------

One detail is missing to make North's multi-linguale fields 
usable in a normal Django project: an possibility to integrate 
these variable fields into your Admin form.

I didn't write this until now because nobody asked me, and 
because Lino has built-in support for North's BabelFields.
See also :ref:`lino:mldbc_tutorial`

