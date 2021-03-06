# Copyright 2013-2014 by Luc Saffre.
# License: BSD, see LICENSE for more details.
"""
This defines the :class:`Site` class.

See :doc:`/settings`.


"""

#~ from __future__ import unicode_literals

import os

from djangosite import Site, DJANGO_DEFAULT_LANGUAGE, assert_django_code
from utils import to_locale, LanguageInfo

gettext_noop = lambda s: s


class NOT_PROVIDED:
    pass


class Site(Site):

    """
    Extends :class:`djangosite.Site`.
    
    
    Instantiating a North Site will automatically set default values for 
    Django's :setting:`SERIALIZATION_MODULES`
    :setting:`FIXTURE_DIRS`
    settings.
    
    """

    is_local_project_dir = False
    """
    This is automatically set when a :class:`Site` is instantiated. 
    Don't override it.
    Contains `True` if this is a "local" project.
    For local projects, Lino checks for local fixtures and config directories
    and adds them to the default settings.
    """

    loading_from_dump = False

    # see docs/settings.rst
    migration_class = None
    languages = None
    hidden_languages = None

    BABEL_LANGS = tuple()

    def init_before_local(self, settings_globals, user_apps):
        if isinstance(user_apps, basestring):
            user_apps = [user_apps]
        user_apps = user_apps + ['north']
        super(Site, self).init_before_local(settings_globals, user_apps)
        self.update_settings(SERIALIZATION_MODULES={
            "py": "north.dpy",
        })

        modname = self.__module__
        i = modname.rfind('.')
        if i != -1:
            modname = modname[:i]
        self.is_local_project_dir = not modname in self.user_apps

        def settings_subdirs(name):
            lst = []
            for p in self.get_settings_subdirs(name):
                if not os.path.exists(os.path.join(p, '..', 'models.py')):
                    lst.append(p.replace(os.sep, "/"))
            return lst

        self.update_settings(FIXTURE_DIRS=tuple(settings_subdirs('fixtures')))
        self.update_settings(LOCALE_PATHS=tuple(settings_subdirs('locale')))

        #~ if not self.is_local_project_dir:
            #~ self.update_settings(
                #~ FIXTURE_DIRS = tuple(self.get_settings_subdirs('fixtures')))
            #~ pth = join(self.project_dir,'fixtures')
            #~ if isdir(pth):
                #~ self.update_settings(FIXTURE_DIRS = [pth])

    def override_defaults(self, **kwargs):
        super(Site, self).override_defaults(**kwargs)
        self.apply_languages()

    def install_migrations(self, *args):
        """
        See :func:`north.dpy.install_migrations`.
        """
        from .dpy import install_migrations
        install_migrations(self, *args)

    def get_used_libs(self, html=None):
        """
        Adds North and Babel to the list of displayed versions.
        """

        import north
        yield ("North", north.SETUP_INFO['version'], north.SETUP_INFO['url'])

        for u in super(Site, self).get_used_libs(html):
            yield u

        import babel
        yield ("Babel", babel.__version__, "http://babel.edgewall.org/")

    def apply_languages(self):
        """
        This function is called when a Site objects get instantiated,
        i.e. while Django is still loading the settings. It analyzes
        the attribute `languages` and converts it to a tuple of
        `LanguageInfo` objects.
        
        """

        if isinstance(self.languages, tuple) \
           and isinstance(self.languages[0], LanguageInfo):
            # e.g. override_defaults() has been called explicitly, without
            # specifying a languages keyword.
            return

        self.language_dict = dict()  # maps simple_code -> LanguageInfo

        self.LANGUAGE_CHOICES = []
        self.LANGUAGE_DICT = dict()  # used in lino.modlib.users
        must_set_language_code = False

        #~ self.AVAILABLE_LANGUAGES = (to_locale(self.DEFAULT_LANGUAGE),)
        if self.languages is None:
            self.languages = [DJANGO_DEFAULT_LANGUAGE]
            #~ self.update_settings(USE_L10N = False)

            #~ info = LanguageInfo(DJANGO_DEFAULT_LANGUAGE,to_locale(DJANGO_DEFAULT_LANGUAGE),0,'')
            #~ self.DEFAULT_LANGUAGE = info
            #~ self.languages = (info,)
            #~ self.language_dict[info.name] = info
        else:
            if isinstance(self.languages, basestring):
                self.languages = self.languages.split()
            #~ lc = [x for x in self.django_settings.get('LANGUAGES' if x[0] in languages]
            #~ lc = language_choices(*self.languages)
            #~ self.update_settings(LANGUAGES = lc)
            #~ self.update_settings(LANGUAGE_CODE = lc[0][0])
            #~ self.update_settings(LANGUAGE_CODE = self.languages[0])
            self.update_settings(USE_L10N=True)
            must_set_language_code = True

        languages = []
        for i, django_code in enumerate(self.languages):
            assert_django_code(django_code)
            name = to_locale(django_code)
            if name in self.language_dict:
                raise Exception("Duplicate name %s for language code %r"
                                % (name, django_code))
            if i == 0:
                suffix = ''
            else:
                suffix = '_' + name
            info = LanguageInfo(django_code, name, i, str(suffix))
            self.language_dict[name] = info
            languages.append(info)

        new_languages = languages
        for info in tuple(new_languages):
            if '-' in info.django_code:
                base, loc = info.django_code.split('-')
                if not base in self.language_dict:
                    self.language_dict[base] = info

                    # replace the complicated info by a simplified one
                    #~ newinfo = LanguageInfo(info.django_code,base,info.index,info.suffix)
                    #~ new_languages[info.index] = newinfo
                    #~ del self.language_dict[info.name]
                    #~ self.language_dict[newinfo.name] = newinfo

        #~ for base,lst in simple_codes.items():
            #~ if len(lst) == 1 and and not base in self.language_dict:
                #~ self.language_dict[base] = lst[0]

        self.languages = tuple(new_languages)
        self.DEFAULT_LANGUAGE = self.languages[0]
        #~ self.BABEL_LANGS = tuple([to_locale(code) for code in self.languages[1:]])
        self.BABEL_LANGS = tuple(self.languages[1:])
        #~ self.AVAILABLE_LANGUAGES = self.AVAILABLE_LANGUAGES + self.BABEL_LANGS

        if must_set_language_code:
            #~ self.update_settings(LANGUAGE_CODE = self.get_default_language())
            self.update_settings(LANGUAGE_CODE=self.languages[0].django_code)
            """
            Note: LANGUAGE_CODE is what *Django* believes to be the default language.
            This should be some variant of English ('en' or 'en-us') 
            if you use `django.contrib.humanize`
            https://code.djangoproject.com/ticket/20059
            """

        self.setup_languages()

    def setup_languages(self):
        """
        Reduce Django's :setting:`LANGUAGES` to my `languages`.
        Note that lng.name are not yet translated, we take these
        from `django.conf.global_settings`.
        """

        from django.conf.global_settings import LANGUAGES
        from django.utils.translation import ugettext_lazy as _

        def langtext(code):
            for k, v in LANGUAGES:
                if k == code:
                    return v
            # returns None if not found

        def _add_language(code, lazy_text):
            self.LANGUAGE_DICT[code] = lazy_text
            self.LANGUAGE_CHOICES.append((code, lazy_text))

        if self.languages is None:

            _add_language(DJANGO_DEFAULT_LANGUAGE, _("English"))

        else:

            for lang in self.languages:
                code = lang.django_code
                text = langtext(code)
                if text is None:
                    # Django doesn't know these
                    if code == 'de-be':
                        text = gettext_noop("German (Belgium)")
                    elif code == 'de-ch':
                        text = gettext_noop("German (Swiss)")
                    elif code == 'de-at':
                        text = gettext_noop("German (Austria)")
                    elif code == 'en-us':
                        text = gettext_noop("American English")
                    else:
                        raise Exception(
                            "Unknown language code %r (must be one of %s)" % (
                                lang.django_code,
                                [x[0] for x in LANGUAGES]))

                text = _(text)
                _add_language(lang.django_code, text)

            """
            Cannot activate the site's default language
            because some test cases in django.contrib.humanize
            rely on en-us as default language
            """
            #~ set_language(self.get_default_language())

            """
            reduce LANGUAGES to my babel languages:
            """
            self.update_settings(
                LANGUAGES=[x for x in LANGUAGES
                           if x[0] in self.LANGUAGE_DICT])

    def get_language_info(self, code):
        """Use this in Python fixtures or tests to test whether a 
        Site instance supports a given language. 
        `code` must be a Django-style language code
        If that specified language
        
        On a site with only one locale of a language (and optionally
        some other languages), you can use only the language code to
        get a tuple of `(django_code, babel_locale)`:
        
        >>> from north import TestSite as Site
        >>> Site(languages="en-us fr de-be de").get_language_info('en')
        LanguageInfo(django_code='en-us', name=u'en_US', index=0, suffix='')
        
        On a site with two locales of a same language (e.g. 'en-us'
        and 'en-gb'), the simple code 'en' yields that first variant:
        
        >>> site = Site(languages="en-us en-gb")
        >>> print site.get_language_info('en')
        LanguageInfo(django_code='en-us', name=u'en_US', index=0, suffix='')

        """
        return self.language_dict.get(code, None)

    def resolve_languages(self, languages):
        """
        This is used by `UserProfile`.
        
        Examples:
        
        >>> from north import TestSite as Site
        >>> lst = Site(languages="en fr de nl et pt").resolve_languages('en fr')
        >>> [i.name for i in lst]
        ['en', 'fr']
        
        You may not specify languages which don't exist on this site:
        
        >>> Site(languages="en fr de").resolve_languages('en nl')
        Traceback (most recent call last):
        ...
        Exception: Unknown language code 'nl' (must be one of ['en', 'fr', 'de'])
        
        
        """
        rv = []
        if isinstance(languages, basestring):
            languages = languages.split()
        for k in languages:
            if isinstance(k, basestring):
                li = self.get_language_info(k)
                if li is None:
                    raise Exception("Unknown language code %r (must be one of %s)" % (
                        k, [li.name for li in self.languages]))
                rv.append(li)
            else:
                assert k in self.languages
                rv.append(k)
        return tuple(rv)

    def language_choices(self, language, choices):
        l = choices.get(language, None)
        if l is None:
            l = choices.get(self.DEFAULT_LANGUAGE)
        return l

    def get_default_language(self):
        """
        The django code of the default language to use in every 
        :class:`LanguageField <north.dbutils.LanguageField>`.
        
        """
        return self.DEFAULT_LANGUAGE.django_code

    def str2kw(self, name, txt,  **kw):
        from django.utils import translation
        for simple, info in self.language_dict.items():
            with translation.override(simple):
                kw[name + info.suffix] = unicode(txt)
        return kw

    def babelkw(self, name, **kw):
        """
        Return a dict with appropriate resolved field names for a
        BabelField `name` and a set of hard-coded values.

        You have some hard-coded multilingual content in a fixture:

        >>> from north import TestSite as Site
        >>> kw = dict(de="Hallo",en="Hello",fr="Salut")

        The field names where this info gets stored depends on the
        Site's `languages` distribution.
        
        >>> Site(languages="de-be en").babelkw('name',**kw)
        {'name_en': 'Hello', 'name': 'Hallo'}
        
        >>> Site(languages="en de-be").babelkw('name',**kw)
        {'name_de_BE': 'Hallo', 'name': 'Hello'}
        
        >>> Site(languages="en-gb de").babelkw('name',**kw)
        {'name_de': 'Hallo', 'name': 'Hello'}
        
        >>> Site(languages="en").babelkw('name',**kw)
        {'name': 'Hello'}
        
        >>> Site(languages="de-be en").babelkw('name',de="Hallo",en="Hello")
        {'name_en': 'Hello', 'name': 'Hallo'}

        In the following example `babelkw` attributes the 
        keyword `de` to the *first* language variant:
        
        >>> Site(languages="de-ch de-be").babelkw('name',**kw)
        {'name': 'Hallo'}
        
        
        """
        d = dict()
        for simple, info in self.language_dict.items():
            v = kw.get(simple, None)
            if v is not None:
                d[name + info.suffix] = v
        return d

    def args2kw(self, name, *args):
        """
        Takes the basename of a BabelField and the values for each language.
        Returns a `dict` mapping the actual fieldnames to their values.
        """
        assert len(args) == len(self.languages)
        kw = {name: args[0]}
        for i, lang in enumerate(self.BABEL_LANGS):
            kw[name + '_' + lang] = args[i + 1]
        return kw

    def field2kw(self, obj, name, **known_values):
        #~ d = { self.DEFAULT_LANGUAGE.name : getattr(obj,name) }
        for lng in self.languages:
            v = getattr(obj, name + lng.suffix, None)
            if v:
                known_values[lng.name] = v
        return known_values

    def field2args(self, obj, name):
        """
        Return a list of the babel values of this field in the order of
        this Site's :attr:`Site.languages` attribute.
        
        """
        return [getattr(obj, name + li.suffix) for li in self.languages]
        #~ l = [ getattr(obj,name) ]
        #~ for lang in self.BABEL_LANGS:
            #~ l.append(getattr(obj,name+'_'+lang))
        #~ return l

    def babelitem(self, *args, **values):
        from django.utils import translation
        if len(args) == 0:
            info = self.language_dict.get(
                translation.get_language(), self.DEFAULT_LANGUAGE)
            default_value = None
            if info == self.DEFAULT_LANGUAGE:
                return values.get(info.name)
            x = values.get(info.name, None)
            if x is None:
                return values.get(self.DEFAULT_LANGUAGE.name)
            return x
        elif len(args) == 1:
            info = self.language_dict.get(translation.get_language(), None)
            if info is None:
                return args[0]
            default_value = args[0]
            return values.get(info.name, default_value)
        raise ValueError("%(values)s is more than 1 default value." %
                         dict(values=args))

    # babel_get(v) = babelitem(**v)

    def babeldict_getitem(self, d, k):
        v = d.get(k, None)
        if v is not None:
            assert type(v) is dict
            return self.babelitem(**v)

    def babelattr(self, obj, attrname, default=NOT_PROVIDED, language=None):
        if language is None:
            from django.utils import translation
            language = translation.get_language()
        info = self.language_dict.get(language, self.DEFAULT_LANGUAGE)
        if info.index != 0:
            v = getattr(obj, attrname + info.suffix, None)
            if v:
                return v
        if default is NOT_PROVIDED:
            return getattr(obj, attrname)
        else:
            return getattr(obj, attrname, default)
        #~ if lang is not None and lang != self.DEFAULT_LANGUAGE:
            #~ v = getattr(obj,attrname+"_"+lang,None)
            #~ if v:
                #~ return v
        #~ return getattr(obj,attrname,*args)


class TestSite(Site):

    """Used to simplify doctest strings because it inserts default values
    for the two first arguments that are mandatory but not used in our
    examples::
    
    >> from north import Site
    >> Site(globals(), ...)
    
    >> from north import TestSite as Site
    >> Site(...)

    """

    def __init__(self, *args, **kwargs):
        kwargs.update(no_local=True)
        g = dict(__file__=__file__)
        g.update(SECRET_KEY="20227")  # see :djangoticket:`20227`
        super(TestSite, self).__init__(g, *args, **kwargs)

        # 20140913 Hack needed for doctests in :mod:`ad`.
        from django.utils import translation
        translation._default = None


