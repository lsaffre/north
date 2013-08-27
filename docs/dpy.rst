.. _dpy:

===============
Python fixtures
===============

A central feature of :ref:`north` is to add **Python fixtures** to a
Django project.

What is a Python fixture?
=========================

You know that a *fixture* is a portion of data (a collection of data records 
in one or several tables) which can be loaded into a database.
Read more about fixtures in the `Providing initial data for models
<https://docs.djangoproject.com/en/dev/howto/initial-data/>`_
article of the Django documentation.
This article says that "fixtures can be written as XML, YAML, 
or JSON documents". 
Well, :ref:`north` adds another format to this list: Python. 
Here is a fictive minimal example::

  from myapp.models import Foo
  def objects():
      yield Foo(name="First")
      yield Foo(name="Second")

A Python fixture is syntactically a normal Python module,
stored in a file ending with `.py` and
designed to being imported and exectued during Django's 
`loaddata <https://docs.djangoproject.com/en/dev/ref/django-admin/#django-admin-loaddata>`_ 
command.

Python fixtures are useful for unit tests, application prototypes and 
demonstrative examples.
See `Playing with Python fixtures 
<http://www.lino-framework.org/tutorials/dumpy.html>`_.

How it works
------------
  
Django will associate the `.py` ending to 
the North deserializer because your
`SERIALIZATION_MODULES 
<https://docs.djangoproject.com/en/dev/ref/settings/#serialization-modules>`_
setting contains `{"py" : "north.dpy"}`.

The North deserializer expects every Python fixture to define 
a global function `objects` which it expects to return 
(or `yield <http://stackoverflow.com/questions/231767/the-python-yield-keyword-explained>`_)
the list of model instances to be added to the database. 

Vocabulary:

- a *serializer* is run by the 
  `dumpdata <https://docs.djangoproject.com/en/dev/ref/django-admin/#dumpdata-appname-appname-appname-model>`_ 
  command and 
  dumps data into a file which can be  used as a fixture.
  
- a *deserializer* is run by 
  `loaddata <https://docs.djangoproject.com/en/dev/ref/django-admin/#django-admin-loaddata>`_ 
  and loads fixtures into the database.

  
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
 
  
