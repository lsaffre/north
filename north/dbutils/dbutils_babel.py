# -*- coding: UTF-8 -*-
# Copyright 2009-2014 by Luc Saffre.
# License: BSD, see LICENSE for more details.

from __future__ import unicode_literals, print_function

import logging
logger = logging.getLogger(__name__)


from django.db import models
from django.conf import settings
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat


#~ babelattr = settings.SITE.babelattr
LANGUAGE_CODE_MAX_LENGTH = 5


def contribute_to_class(field, cls, fieldclass, **kw):
    if cls._meta.abstract:
        return
    kw.update(blank=True)
    for lang in settings.SITE.BABEL_LANGS:
        kw.update(verbose_name=string_concat(
            field.verbose_name, ' (' + lang.django_code + ')'))
        newfield = fieldclass(**kw)
        #~ newfield._lino_babel_field = True
        # used by dbtools.get_data_elems
        newfield._lino_babel_field = field.name
        newfield._babel_language = lang
        cls.add_to_class(field.name + '_' + lang.name, newfield)


class BabelCharField(models.CharField):

    """
    Define a variable number of `CharField` database fields, 
    one for each language of your :attr:`north.Site.languages`.
    See :ref:`mldbc`.
    """

    def contribute_to_class(self, cls, name):
        super(BabelCharField, self).contribute_to_class(cls, name)
        contribute_to_class(self, cls, models.CharField,
                            max_length=self.max_length)
        #~ kw = dict()
        #~ kw.update(max_length=self.max_length)
        #~ kw.update(blank=True)
        #~ for lang in BABEL_LANGS:
            #~ kw.update(verbose_name=self.verbose_name + ' ('+lang+')')
            #~ newfield = models.CharField(**kw)
            # ~ newfield._lino_babel_field = True # used by dbtools.get_data_elems
            #~ cls.add_to_class(self.name + '_' + lang,newfield)


class BabelTextField(models.TextField):

    """
    Define a variable number of `TextField` database fields, 
    one for each language of your :attr:`north.Site.languages`.
    See :ref:`mldbc`.
    """

    def contribute_to_class(self, cls, name):
        super(BabelTextField, self).contribute_to_class(cls, name)
        contribute_to_class(self, cls, models.TextField)


class BabelNamed(models.Model):

    """
    Mixin for models that have a babel field `name` 
    (labelled "Description") for each language.
    
    See usage example in :ref:`mldbc_tutorial`.
    """

    class Meta:
        abstract = True
        # ~ app_label = 'unused' # avoid "IndexError: list index out of range" in `django/db/models/base.py`
        # cannot set app_label here because subclasses without their own Meta
        # would inherit it

    name = BabelCharField(max_length=200, verbose_name=_("Designation"))

    def __unicode__(self):
        return settings.SITE.babelattr(self, 'name')


class LanguageField(models.CharField):

    """A field that lets the user select a language from the available
    babel languages.

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
        models.CharField.__init__(self, *args, **defaults)


def run_with_language(lang, func):
    """Selects the specified language `lang`, calls the specified
    function `func`, restores the previously selected language.
    
    Deprecated: use translation.override() instead of this.

    """
    with translation.override(lang):
        return func()

    #~ current_lang = get_language()
    #~ set_language(lang)
    #~ try:
        #~ rv = func()
    #~ except Exception:
        #~ set_language(current_lang)
        #~ raise
    #~ set_language(current_lang)
    #~ return rv


LOOKUP_OP = '__iexact'


def lookup_filter(fieldname, value, **kw):
    """
    Return a `models.Q` to be used if you want to search for a given 
    string in any of the languages for the given babel field.
    """
    kw[fieldname + LOOKUP_OP] = value
    #~ kw[fieldname] = value
    flt = models.Q(**kw)
    del kw[fieldname + LOOKUP_OP]
    for lng in settings.SITE.BABEL_LANGS:
        kw[fieldname + lng.suffix + LOOKUP_OP] = value
        flt = flt | models.Q(**kw)
        del kw[fieldname + lng.suffix + LOOKUP_OP]
    return flt
