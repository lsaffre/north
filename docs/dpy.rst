.. _dpy:

===============
Python fixtures
===============

A central feature of `django-north` is to
define a serializer/deserializer for **Python fixtures**.

.. contents:: Table of Contents
   :depth: 2
   :local:

What is a Python fixture?
=========================

A fixture is a portion of data (a collection of data records 
in one or several tables) which can be loaded into a database.
Read more about fixtures in the `Providing initial data for models
<https://docs.djangoproject.com/en/dev/howto/initial-data/>`_
article of the Django documentation.
This article also says that "fixtures can be written as XML, YAML, 
or JSON documents". 
North adds another format to this list: Python. 


A Python fixture is syntactically a normal Python module,
stored in a file ending with `.py` and
designed to being imported and exectued during Django's 
`loaddata <https://docs.djangoproject.com/en/dev/ref/django-admin/#django-admin-loaddata>`_ 
command.
Django will associate the `.py` ending to 
the North deserializer because your
`SERIALIZATION_MODULES 
<https://docs.djangoproject.com/en/dev/ref/settings/#serialization-modules>`_
setting contains `{"py" : "north.dpy"}`.

The North deserializer expects every Python fixture to define 
a global function `objects` which it expects to return 
(or `yield <http://stackoverflow.com/questions/231767/the-python-yield-keyword-explained>`_)
the list of model instances to be added to the database. 

A fictive minimal Example::

  from myapp.models import Foo
  def objects():
      yield Foo(name="First")
      yield Foo(name="Second")
      
Vocabulary:

- a *serializer* is run by the 
  `dumpdata <https://docs.djangoproject.com/en/dev/ref/django-admin/#dumpdata-appname-appname-appname-model>`_ 
  command and 
  dumps data into a file which can be  used as a fixture.
  
- a *deserializer* is run by 
  `loaddata <https://docs.djangoproject.com/en/dev/ref/django-admin/#django-admin-loaddata>`_ 
  and loads fixtures into the database.

      
      
What are Python fixtures good for?
==================================
      
There are two big use cases for Python fixtures: 

(1) "dumped" fixtures are used for backup and `database migration`_.

    You dump the content of a database to a python script
    which can be loaded on another machine 
    to reproduce an exact duplicate of the original database.
  

(2) `Intelligent fixtures`_ are reusable sets of data 
    to be used by unit tests, application prototypes and 
    demonstrative examples.

.. _backup:
    
Backup
======

You can make a Python dump of your database
using 
the :mod:`dump2py <north.management.commands.dump2py>` 
management command that comes with :mod:`north`.
  
For example::
  
    $ python manage.py dump2py 20130117
    
This will create a directory `20130117` with a set of ` .py` files 
which are a perfect representation, in Python, of your database at 
that moment.
These files contain a complete backup of your database. 
You can archive the directory and send it around per email.
  
  
To restore such a dump to your database, simply run the 
:xfile:`restore.py` 
script from that directory::
  
      $ python manage.py run mydump/restore.py
  
Or, if you don't use per-project :xfile:`manage.py` files::
      
      $ set DJANGO_SETTINGS_MODULE=myproject
      $ django-admin.py run mydump/restore.py
  
Note that we are using here the 
:mod:`run <djangosite.management.commands.run>` 
management command.
This makes it possible to restore your data into another 
project, creating a copy of your database.
  

.. _datamig:
    
Database Migration
==================

When you upgrade to a newer version of 
a North application, or when you change 
certain parameters in your local :xfile:`settings.py`,
then this might require **changes in the database structure**.
This is called database migration.

How to migrate data
-------------------

A Python dump makes life easy
for the system administrator who does an upgrade 
of your application.

- Before upgrading or applying configuration changes, 
  create a backup as described above.
  
- After upgrading or applying configuration changes, 
  restore your database from that dump.
  This will automatically detect version changes and 
  apply any necessary changes to your data.

It is of course recommended to stop any other processes 
which might access your database during the whole procedure.


The Double Dump Test (DDT)
--------------------------

When :mod:`initdb
<djangosite.management.commands.initdb>` 
successfully terminated without any warnings 
and error messages, 
then there are good chances 
that your database has been successfully migrated. 

But here is one more automated test that you may run 
when everything seems okay.

This so-called :ref:`ddt` consists of the following steps:

- make another dump :file:`a.py` of the freshly migrated database 
- load this dump to the database
- make a third dump :file:`b.py` of your database 
- Compare the files :file:`a.py` and :file:`b.py`:
  if there's no difference, then the double dump test succeeded!


For example, here is a successful upgrade with data migration::
  
  $ python manage.py dumpdata --format py > fixtures/d20110931.py
  $ ./pull # update to new Lino version
  $ python manage.py initdb d20110931 --noinput
  INFO Lino initdb ('d20110901a',) started on database mysite.
  Creating tables ...
  Installing custom SQL ...
  Installing indexes ...
  (...)
  INFO Saved 29798 instances from /usr/local/django/mysite/fixtures/d20110901a.py.
  Installed 29798 object(s) from 1 fixture(s)
  INFO Lino initdb done ('d20110901a',) on database mysite.  
  $
  

Now run the additional test::  
  
  $ python manage.py dumpdata --format py > fixtures/a.py
  $ python manage.py initdb a --noinput
  $ python manage.py dumpdata --format py > fixtures/b.py
  $ diff fixtures/a.py fixtures/b.py
  
If there's no difference between the two dumps, then the test succeeded!
  
.. note:: 

  With versions before 20110901 there were still 
  differences if your database contained records with 
  `auto_now 
  <https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.DateField.auto_now>`_
  fields.
  
  
Designing data migrations for your application
----------------------------------------------

Designing data migrations for your application
is easy but not yet well documented.

The main trick is the last line of any Python fixture::

    settings.SITE.install_migrations(globals())

This means that the fixture itself will call 
the :func:`install_migrations <north.dpy.install_migrations>` 
method of your new application *before* actually starting to yield 
any database object.
And it passes her `globals()` dict, which means 
that you can potentially change everything.

Look at the source code of 
:mod:`lino_welfare.migrate`
and
:mod:`lino_welfare.old_migrate`.

A magical `before_dumpy_save` attribute may contain custom 
code to apply inside the try...except block. 
If that code fails, the deserializer will simply 
defer the save operation and try it again.
    
Intelligent fixtures
====================

See `Playing with intelligent Python fixtures 
<http://www.lino-framework.org/tutorials/dumpy.html>`_.
  
  
Discussion
==========  

Concept and implementation of Python fixtures is fully the author's work, 
and we didn't yet find a similar approach in any other framework.

But the basic idea of using Python language to describe data collections 
is of course not new. For example Limodou published a Djangosnippet 
in 2007 which does something similar:
`db_dump.py - for dumpping and loading data from database
<http://djangosnippets.org/snippets/14/>`_.



See also
--------

- :doc:`/tutorials/polls/mysite/index`
- http://code.djangoproject.com/ticket/10664
 
Note about `django-extensions <https://github.com/django-extensions>`_ 
----------------------------------------------------------------------

`django-extensions <https://github.com/django-extensions>`_ 
has a command "dumpscript" which is comparable.
Differences: 

- dumpy produces fixtures to be restored with loaddata,
  dumpscript produces a simple python script to be restored with runscript
- the fixtures generated by dumpy are designed in order to make it possible to 
  write automated data migrations.
  
  
Models that get special handling
--------------------------------

- `ContentType` objects aren't stored in a dump because they 
  can always be recreated.
- `Site` and `Permission` objects *must* be stored and *must not* be re-created
- `Session` objects can get lost in a dump and are not stored.


