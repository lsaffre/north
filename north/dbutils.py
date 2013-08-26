# -*- coding: UTF-8 -*-
"""
Generic support for :ref:`mldbc`.

:copyright: Copyright 2009-2013 by Luc Saffre.
:license: BSD, see LICENSE for more details.


This includes definition of *babel fields* in your Django Models 
as well as methods to access these fields.

Babel fields are fields defined using 
:class:`BabelCharField`
or
:class:`BabelTextField`.

Each babel field generates a series of normal CharFields (or TextFields) 
depending on your :attr:`languages <north.Site.languages>` setting.

Example::

  class Foo(models.Model):
      name = BabelCharField(_("Foo"), max_length=200)
      
      
This module also defines the model mixin :class:`BabelNamed`
      

Date formatting functions
-------------------------

This module also includes shortcuts to `python-babel`'s 
`date formatting functions <http://babel.pocoo.org/docs/dates/>`_

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
from django.utils.translation import string_concat

from djangosite.dbutils import monthname, set_language
from djangosite.dbutils import dtomy # obsolete
from djangosite.dbutils import fdmy

import north

LANGUAGE_CODE_MAX_LENGTH = 5


#~ dtos = settings.SITE.dtos
#~ dtosl = settings.SITE.dtosl
#~ set_language = settings.SITE.set_language
#~ kw2fields = settings.SITE.kw2fields
babelkw = settings.SITE.babelkw
field2kw = settings.SITE.field2kw
babel_values = settings.SITE.babelkw # old alias for backwards compatibility
babelattr = settings.SITE.babelattr
babelitem = settings.SITE.babelitem
#~ getattr_lang = babelattr
    





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
    def __init__(self,model_spec,app_label):
        self.model_spec = model_spec
        self.app_label = app_label
        #~ print(self)
        
    def __repr__(self):
        return self.__class__.__name__ + '(%s,%s)' % (self.model_spec,self.app_label)
        
    #~ def __getattr__(self,name):
        #~ raise AttributeError("%s has no attribute %r" % (self,name))

#~ def resolve_model(model_spec,app_label=None,strict=False,seed_cache=True):
def resolve_model(model_spec,app_label=None,strict=False):
    """
    Return the class object of the specified model.
    This works also in combination  with :attr:`lino.Site.override_modlib_models`,
    so you don't need to worry about where the real class definition is.
    
    Attention: this function **does not** trigger a loading of Django's 
    model cache, so you should not use it at module-level unless you 
    know what you do.
    
    For example,    
    ``dd.resolve_model("contacts.Person")`` 
    will return the `Person` model 
    even if the concrete Person model is not defined 
    in :mod:`lino.modlib.contacts.models` because it is in
    :attr:`lino.Site.override_modlib_models`.
    
    See also django.db.models.fields.related.add_lazy_relation()
    """
    #~ models.get_apps() # trigger django.db.models.loading.cache._populate()
    if isinstance(model_spec,basestring):
        if '.' in model_spec:
            app_label, model_name = model_spec.split(".")
        else:
            model_name = model_spec
            
        #~ try:
            #~ app_label, model_name = model_spec.split(".")
        #~ except ValueError:
            #~ # If we can't split, assume a model in current app
            #~ #app_label = rpt.app_label
            #~ model_name = model_spec
            
        model = models.get_model(app_label,model_name,seed_cache=False)
        #~ model = models.get_model(app_label,model_name,seed_cache=seed_cache)
    else:
        model = model_spec
    if not isinstance(model,type) or not issubclass(model,models.Model):
        if strict:
            if False:
                from django.db.models import loading
                print(20130219, settings.INSTALLED_APPS)
                print(loading.get_models())
                #~ if len(loading.cache.postponed) > 0:
              
            if isinstance(strict,basestring):
                raise Exception(strict % model_spec)
            raise ImportError(
                "resolve_model(%r,app_label=%r) found %r (settings %s)" % (
                model_spec,app_label,model,settings.SETTINGS_MODULE))
        #~ logger.info("20120628 unresolved %r",model)
        return UnresolvedModel(model_spec,app_label)
    return model
    
def old_resolve_model(model_spec,app_label=None,strict=False):
    """
    doesn't work for contacts.Company because the model is defined somewhere else.
    """
    models.get_apps() # trigger django.db.models.loading.cache._populate()
    if isinstance(model_spec,basestring):
        if '.' in model_spec:
            app_label, model_name = model_spec.split(".")
        else:
            model_name = model_spec
        app = resolve_app(app_label)
        model = getattr(app,model_name,None)
    else:
        model = model_spec
    if not isinstance(model,type) or not issubclass(model,models.Model):
        if strict:
            raise Exception(
                "resolve_model(%r,app_label=%r) found %r (settings %s)" % (
                model_spec,app_label,model,settings.SETTINGS_MODULE))
        return UnresolvedModel(model_spec,app_label)
    return model
    


def contribute_to_class(field,cls,fieldclass,**kw):
    if cls._meta.abstract:
        return
    kw.update(blank=True)
    for lang in settings.SITE.BABEL_LANGS:
        kw.update(verbose_name=string_concat(field.verbose_name,' ('+lang.django_code+')'))
        newfield = fieldclass(**kw)
        #~ newfield._lino_babel_field = True 
        newfield._lino_babel_field = field.name # used by dbtools.get_data_elems
        newfield._babel_language = lang 
        cls.add_to_class(field.name + '_' + lang.name,newfield)

class BabelCharField(models.CharField):
    """
    Define a variable number of clones of the "master" field, 
    one for each language of your :attr:`djangosite.Site.languages`.
    """
        
    def contribute_to_class(self, cls, name):
        super(BabelCharField,self).contribute_to_class(cls, name)
        contribute_to_class(self,cls,models.CharField,
            max_length=self.max_length)
        #~ kw = dict()
        #~ kw.update(max_length=self.max_length)
        #~ kw.update(blank=True)
        #~ for lang in BABEL_LANGS:
            #~ kw.update(verbose_name=self.verbose_name + ' ('+lang+')')
            #~ newfield = models.CharField(**kw)
            #~ newfield._lino_babel_field = True # used by dbtools.get_data_elems
            #~ cls.add_to_class(self.name + '_' + lang,newfield)
            

class BabelTextField(models.TextField):
    """
    Define a variable number of clones of the "master" field, 
    one for each babel language.
    """
    def contribute_to_class(self, cls, name):
        super(BabelTextField,self).contribute_to_class(cls, name)
        contribute_to_class(self,cls,models.TextField)


                
class BabelNamed(models.Model):
    """
    Mixin for models that have a babel field `name` 
    (labelled "Description") for each language.
    
    See usage example in :ref:`mldbc_tutorial`.
    """
    
    class Meta:
        abstract = True
        app_label = 'unused' # avoid "IndexError: list index out of range" in `django/db/models/base.py`
        
    name = BabelCharField(max_length=200,verbose_name=_("Designation"))
    
    def __unicode__(self):
        return babelattr(self,'name')
    
            
                
class LanguageField(models.CharField):
    """
    A field that lets the user select 
    a language from the available babel languages.
    """
    def __init__(self, *args, **kw):
        defaults = dict(
            verbose_name=_("Language"),
            choices=iter(settings.SITE.LANGUAGE_CHOICES),
            default=settings.SITE.get_default_language,
            #~ default=get_language,
            max_length=LANGUAGE_CODE_MAX_LENGTH,
            )
        defaults.update(kw)
        models.CharField.__init__(self,*args, **defaults)

                
def run_with_language(lang,func):                
    """
    Selects the specified language `lang`, 
    calls the specified functon `func`,
    restores the previously selected language.
    """
    current_lang = get_language()
    set_language(lang)
    try:
        rv = func()
    except Exception:
        set_language(current_lang)
        raise
    set_language(current_lang)
    return rv
                
                
LOOKUP_OP = '__iexact'

def lookup_filter(fieldname,value,**kw):
    """
    Return a `models.Q` to be used if you want to search for a given 
    string in any of the languages for the given babel field.
    """
    kw[fieldname+LOOKUP_OP] = value
    #~ kw[fieldname] = value
    flt = models.Q(**kw)
    del kw[fieldname+LOOKUP_OP]
    for lng in settings.SITE.BABEL_LANGS:
        kw[fieldname+lng.suffix+LOOKUP_OP] = value
        #~ flt = flt | models.Q(**{self.lookup_field.name+'_'+lng+'__iexact': value})
        #~ flt = flt | models.Q(**{self.lookup_field.name+'_'+lng: value})
        flt = flt | models.Q(**kw)
        del kw[fieldname+lng.suffix+LOOKUP_OP]
    return flt

    
    
                        

def format_date(d,format='medium'):
    if not d: return ''
    return babel_format_date(d, format=format,
        locale=north.to_locale(translation.get_language()))
    
def dtos(d):
    return format_date(d, format='short')
    
def dtosm(d):
    return format_date(d,format='medium')
        
def dtosl(d):
    return format_date(d, format='full')
    
def fdf(d): 
    return format_date(d, format='full')
def fdl(d): return format_date(d, format='long')
def fdm(d): return format_date(d, format='medium')
def fds(d): return format_date(d, format='short')
    
def day_and_month(d):
    return format_date(d,"dd. MMMM")
    
