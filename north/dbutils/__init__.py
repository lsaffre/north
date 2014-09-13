# -*- coding: UTF-8 -*-
# Copyright 2009-2014 by Luc Saffre.
# License: BSD, see LICENSE for more details.
"""Generic support for :ref:`mldbc`.

This includes definition of *babel fields* in your Django Models as
well as methods to access these fields.

Babel fields are fields defined using :class:`BabelCharField` or
:class:`BabelTextField`.

Each babel field generates a series of normal CharFields (or
TextFields) depending on your :setting:`languages` setting.

Example::

  class Foo(models.Model):
      name = BabelCharField(_("Foo"), max_length=200)
      
      
This module also defines the model mixin :class:`BabelNamed`
      

Date formatting functions
-------------------------

This module also includes shortcuts to `python-babel`'s `date
formatting functions <http://babel.pocoo.org/docs/dates/>`_

>>> d = datetime.date(2013,8,26)
>>> print(fds(d)) # short
8/26/13
>>> print(fdm(d)) # medium
Aug 26, 2013
>>> print(fdl(d)) # long
August 26, 2013
>>> print(fdf(d)) # full
Monday, August 26, 2013

"""

from __future__ import unicode_literals, print_function

import logging
logger = logging.getLogger(__name__)

import sys
import locale
import datetime

from babel.dates import format_date as babel_format_date

from django.db import models
from django.conf import settings


from django.db import models
from django.conf import settings
from django.utils import translation
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _

from djangosite import AFTER17
from djangosite.dbutils import monthname
#~ from djangosite.dbutils import set_language
from djangosite.dbutils import dtomy  # obsolete. use fdmy instead
from djangosite.dbutils import fdmy

from north.dbutils.dbutils_babel import BabelCharField, BabelTextField, BabelNamed
from north.dbutils.dbutils_babel import LanguageField
from north.dbutils.dbutils_babel import run_with_language
from north.dbutils.dbutils_babel import lookup_filter
from north.dbutils.dbutils_babel import contribute_to_class
from north.dbutils.dbutils_babel import LANGUAGE_CODE_MAX_LENGTH

from north.utils import to_locale

def babelkw(*args, **kw):
    return settings.SITE.babelkw(*args, **kw)


def babelattr(*args, **kw):
    return settings.SITE.babelattr(*args, **kw)
babel_values = babelkw  # old alias for backwards compatibility


class UnresolvedModel:

    """
    This is the object returned by :func:`resolve_model` 
    if the specified model is not installed.
    
    We don't want resolve_model to raise an Exception because there are 
    cases of :ref:`datamig` where it would disturb. 
    Asking for a non-installed model is not a sin, but trying to use it is.
    
    I didn't yet bother very much about finding a way to make the 
    model_spec appear in error messages such as
    ``AttributeError: UnresolvedModel instance has no attribute '_meta'``.
    Current workaround is to uncomment the ``print`` statement 
    below in such situations...
    
    """

    def __init__(self, model_spec, app_label):
        self.model_spec = model_spec
        self.app_label = app_label
        #~ print(self)

    def __repr__(self):
        return self.__class__.__name__ + '(%s,%s)' % (self.model_spec, self.app_label)

    #~ def __getattr__(self,name):
        #~ raise AttributeError("%s has no attribute %r" % (self,name))

#~ def resolve_model(model_spec,app_label=None,strict=False,seed_cache=True):


def resolve_model(model_spec, app_label=None, strict=False):
    """Return the class object of the specified model.  This works also in
    combination with :attr:`ad.Site.override_modlib_models`, so you
    don't need to worry about where the real class definition is.
    
    Attention: this function **does not** trigger a loading of
    Django's model cache, so you should not use it at module-level
    unless you know what you do.
    
    For example, ``dd.resolve_model("contacts.Person")`` will return
    the `Person` model even if the concrete Person model is not
    defined in :mod:`lino.modlib.contacts.models` because it is in
    :attr:`dd.Site.override_modlib_models`.
    
    See also django.db.models.fields.related.add_lazy_relation()

    """
    # ~ models.get_apps() # trigger django.db.models.loading.cache._populate()
    if isinstance(model_spec, basestring):
        if '.' in model_spec:
            app_label, model_name = model_spec.split(".")
        else:
            model_name = model_spec

        if AFTER17:
            from django.apps import apps
            model = apps.get_model(app_label, model_name)
        else:
            model = models.get_model(app_label, model_name, seed_cache=False)
        #~ model = models.get_model(app_label,model_name,seed_cache=seed_cache)
    else:
        model = model_spec
    if not isinstance(model, type) or not issubclass(model, models.Model):
        if strict:
            if False:
                from django.db.models import loading
                print(20130219, settings.INSTALLED_APPS)
                print(loading.get_models())
                #~ if len(loading.cache.postponed) > 0:

            if isinstance(strict, basestring):
                raise Exception(strict % model_spec)
            raise ImportError(
                #~ "resolve_model(%r,app_label=%r) found %r (settings %s)" % (
                "resolve_model(%r,app_label=%r) found %r (settings %s, INSTALLED_APPS=%s)" % (
                    #~ model_spec,app_label,model,settings.SETTINGS_MODULE))
                    model_spec, app_label, model, settings.SETTINGS_MODULE, settings.INSTALLED_APPS))
        #~ logger.info("20120628 unresolved %r",model)
        return UnresolvedModel(model_spec, app_label)
    return model


def old_resolve_model(model_spec, app_label=None, strict=False):
    """
    doesn't work for contacts.Company because the model is defined somewhere else.
    """
    models.get_apps()  # trigger django.db.models.loading.cache._populate()
    if isinstance(model_spec, basestring):
        if '.' in model_spec:
            app_label, model_name = model_spec.split(".")
        else:
            model_name = model_spec
        app = resolve_app(app_label)
        model = getattr(app, model_name, None)
    else:
        model = model_spec
    if not isinstance(model, type) or not issubclass(model, models.Model):
        if strict:
            raise Exception(
                "resolve_model(%r,app_label=%r) found %r (settings %s)" % (
                    model_spec, app_label, model, settings.SETTINGS_MODULE))
        return UnresolvedModel(model_spec, app_label)
    return model


def format_date(d, format='medium'):
    if not d:
        return ''
    return babel_format_date(d, format=format,
                             locale=to_locale(translation.get_language()))

#~ def dtos(d):
    #~ return format_date(d, format='short')

#~ def dtosm(d):
    #~ return format_date(d,format='medium')

#~ def dtosl(d):
    #~ return format_date(d, format='full')


def fdf(d):
    return format_date(d, format='full')


def fdl(d):
    return format_date(d, format='long')


def fdm(d):
    return format_date(d, format='medium')


def fds(d):
    return format_date(d, format='short')

# backwards compatibility:
dtosl = fdf
dtosm = fdm
dtos = fds


def day_and_month(d):
    return format_date(d, "dd. MMMM")
