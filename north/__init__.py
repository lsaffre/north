"""
:copyright: Copyright 2013 by Luc Saffre.
:license: BSD, see LICENSE for more details.
"""

import os

from djangosite import Site, DJANGO_DEFAULT_LANGUAGE, assert_django_code
#~ from north.babel import BabelSiteMixin
#~ from north.babel import Site

#~ execfile(os.path.join(os.path.dirname(__file__),'version.py'))
execfile(os.path.join(os.path.dirname(__file__),'setup_info.py'))
#~ execfile(os.path.join(os.path.dirname(__file__),'..','setup_info.py'))

__version__ = SETUP_INFO['version'] # 

intersphinx_url = "http://north.lino-framework.org"

#~ __author__ = "Luc Saffre <luc.saffre@gmx.net>"

#~ __url__ = "http://lino.saffre-rumma.net"
#~ __url__ = "http://code.google.com/p/lino/"
#~ __url__ = "http://north.lino-framework.org"


#~ __copyright__ = "Copyright (c) 2002-2013 Luc Saffre."


#~ gettext = lambda s: s

#~ # todo: remove this
#~ def language_choices(*args):
    #~ """
    #~ A subset of Django's LANGUAGES.
    #~ See :doc:`/blog/2011/0226`.
    #~ """
    #~ _langs = dict(
        #~ en=gettext('English'),
        #~ de=gettext('German'),
        #~ fr=gettext('French'),
        #~ nl=gettext('Dutch'),
        #~ et=gettext('Estonian'),
    #~ )
    #~ return [(x,_langs[x]) for x in args]


#~ LANGUAGE_CODE_MAX_LENGTH = 2
#~ """
#~ """

#~ def simplified_code(code):
    #~ """
    #~ We store only the main code, supposing that nobody maintains
    #~ multilingual database content for different variants of the 
    #~ same language.
    #~ """
    #~ return code[:LANGUAGE_CODE_MAX_LENGTH].strip()

#~ DEFAULT_LANGUAGE = simplified_code(settings.LANGUAGE_CODE)

import collections
LanguageInfo = collections.namedtuple('LanguageInfo', ('django_code','name','index','suffix'))



gettext_noop = lambda s: s

def to_locale(language):
    """
    Simplified copy of `django.utils.translation.to_locale`, but we 
    need it while the `settings` module is being loaded, i.e. we 
    cannot yet import django.utils.translation.
    Also we don't need the to_lower argument.
    """
    p = language.find('-')
    if p >= 0:
        # Get correct locale for sr-latn
        if len(language[p+1:]) > 2:
            return language[:p].lower()+'_'+language[p+1].upper()+language[p+2:].lower()
        return language[:p].lower()+'_'+language[p+1:].upper()
    else:
        return language.lower() 
        

class NOT_PROVIDED: pass


class Site(Site):
    """
    Extends :class:`djangosite.Site`
    by adding some attributes and methods used by `north`.
    
    Instantiating a North Site will automatically set default values for 
    Django's :setting:`SERIALIZATION_MODULES`
    :setting:`FIXTURE_DIRS`
    settings.
    
    """
    
    is_local_project_dir = False
    """
    This is automatically set when a :class:`Lino` is instantiated. 
    Don't override it.
    Contains `True` if this is a "local" project.
    For local projects, Lino checks for local fixtures and config directories
    and adds them to the default settings.
    """
    
    migration_module = None
    """
    If you maintain a data migration module for your application, 
    specify its name here.
    """
    
    loading_from_dump = False
    """
    Set to `False` by python dumps that were generated by
    :meth:`lino.utils.dumpy.Serializer.serialize`.
    Used in 
    :func:`lino.modlib.cal.models.update_auto_task`
    and
    :mod:`lino.modlib.mails.models`.
    """
    
    
    languages = None 
    """
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
    and thus require a data migration.
    
    If this is not None, Site will 
    set the Django settings :setting:`USE_L10N` 
    and  :setting:`LANGUAGE_CODE`.
    
    """
    
    BABEL_LANGS = tuple()
    
    
    def init_before_local(self,*args):
        super(Site,self).init_before_local(*args)
        self.update_settings(SERIALIZATION_MODULES = {
            "py" : "north.dpy",
        })
        
        modname = self.__module__
        i = modname.rfind('.')
        if i != -1:
            modname = modname[:i]
        self.is_local_project_dir = not modname in self.user_apps
        
        def settings_subdirs(name):
            lst = []
            for p in self.get_settings_subdirs(name):
                if not os.path.exists(os.path.join(p,'..','models.py')):
                    lst.append(p.replace(os.sep,"/"))
            return lst
        
        self.update_settings(FIXTURE_DIRS=tuple(settings_subdirs('fixtures')))
        self.update_settings(LOCALE_PATHS=tuple(settings_subdirs('locale')))
            
        #~ if not self.is_local_project_dir:
            #~ self.update_settings(
                #~ FIXTURE_DIRS = tuple(self.get_settings_subdirs('fixtures')))
            #~ pth = join(self.project_dir,'fixtures')
            #~ if isdir(pth):
                #~ self.update_settings(FIXTURE_DIRS = [pth])
                
        
    def override_defaults(self,**kwargs):
        super(Site,self).override_defaults(**kwargs)
        self.apply_languages()
    
    
    def install_migrations(self,*args):
        """
        See :func:`north.dpy.install_migrations`.
        """
        from .dpy import install_migrations
        install_migrations(self,*args)
        
          
    def using(self,ui=None):
        """
        
        """
        for u in super(Site,self).using(ui): yield u
        import babel
        
        yield ("Babel",babel.__version__,"http://babel.edgewall.org/")
        #~ yield (SETUP_INFO['name'],SETUP_INFO['version'],SETUP_INFO['url'])
        
   
    def apply_languages(self):
        """
        This function is called when a Site objects get instantiated,
        i.e. while Django is still loading the settings. It analyzes 
        the attribute `languages` and converts it to a tuple of 
        `LanguageInfo` objects.
        
        >>> from north import TestSite as Site
        >>> from pprint import pprint
        >>> pprint(Site().django_settings) #doctest: +ELLIPSIS
        {'DATABASES': {'default': {'ENGINE': 'django.db.backends.sqlite3',
                                   'NAME': '...default.db'}},
         'FIXTURE_DIRS': (),
         'INSTALLED_APPS': ('djangosite',),
         'LOCALE_PATHS': (),
         'SECRET_KEY': '20227',
         'SERIALIZATION_MODULES': {'py': 'north.dpy'},
         '__file__': '...'}
     
        >>> pprint(Site(languages="en fr de").languages)
        (LanguageInfo(django_code='en', name='en', index=0, suffix=''),
         LanguageInfo(django_code='fr', name='fr', index=1, suffix='_fr'),
         LanguageInfo(django_code='de', name='de', index=2, suffix='_de'))
        
        >>> pprint(Site(languages="de-ch de-be").languages)
        (LanguageInfo(django_code='de-ch', name='de_CH', index=0, suffix=''),
         LanguageInfo(django_code='de-be', name='de_BE', index=1, suffix='_de_BE'))
        
        If we have more than languages en-us and en-gb *on a same Site*, 
        then it is not allowed to specify just "en". 
        But in most cases it is allowed to just say "en", which will 
        mean "the English variant used on this Site".
        
        >>> site = Site(languages="en-us fr de-be de")
        >>> pprint(site.languages)
        (LanguageInfo(django_code='en-us', name='en_US', index=0, suffix=''),
         LanguageInfo(django_code='fr', name='fr', index=1, suffix='_fr'),
         LanguageInfo(django_code='de-be', name='de_BE', index=2, suffix='_de_BE'),
         LanguageInfo(django_code='de', name='de', index=3, suffix='_de'))
        
        >>> pprint(site.language_dict)
        {'de': LanguageInfo(django_code='de', name='de', index=3, suffix='_de'),
         'de_BE': LanguageInfo(django_code='de-be', name='de_BE', index=2, suffix='_de_BE'),
         'en': LanguageInfo(django_code='en-us', name='en_US', index=0, suffix=''),
         'en_US': LanguageInfo(django_code='en-us', name='en_US', index=0, suffix=''),
         'fr': LanguageInfo(django_code='fr', name='fr', index=1, suffix='_fr')}
        
        """
        
        if isinstance(self.languages,tuple) and isinstance(self.languages[0],LanguageInfo):
            # e.g. override_defaults() has been called explicitly, without specifying a languages keyword.
            return 
            
        self.language_dict = dict() # maps simple_code -> LanguageInfo
        
        self.LANGUAGE_CHOICES = []
        self.LANGUAGE_DICT = dict() # used in lino.modlib.users
        must_set_language_code = False
        
        #~ self.AVAILABLE_LANGUAGES = (to_locale(self.DEFAULT_LANGUAGE),)
        if self.languages is None:
            self.languages = [ DJANGO_DEFAULT_LANGUAGE ]
            #~ self.update_settings(USE_L10N = False)
            
            #~ info = LanguageInfo(DJANGO_DEFAULT_LANGUAGE,to_locale(DJANGO_DEFAULT_LANGUAGE),0,'')
            #~ self.DEFAULT_LANGUAGE = info
            #~ self.languages = (info,)
            #~ self.language_dict[info.name] = info
        else:
            if isinstance(self.languages,basestring):
                self.languages = self.languages.split()
            #~ lc = [x for x in self.django_settings.get('LANGUAGES' if x[0] in languages]
            #~ lc = language_choices(*self._languages)
            #~ self.update_settings(LANGUAGES = lc)
            #~ self.update_settings(LANGUAGE_CODE = lc[0][0])
            #~ self.update_settings(LANGUAGE_CODE = self.languages[0])
            self.update_settings(USE_L10N = True)
            must_set_language_code = True
          
        languages = []
        for i,django_code in enumerate(self.languages):
            assert_django_code(django_code)
            name = to_locale(django_code)
            if name in self.language_dict:
                raise Exception("Duplicate name %s for language code %r" 
                    % (name,django_code))
            if i == 0: 
                suffix = ''
            else:
                suffix = '_' + name
            info = LanguageInfo(django_code,name,i,suffix)
            self.language_dict[name] = info
            languages.append(info)
            
        new_languages = languages
        for info in tuple(new_languages):
            if '-' in info.django_code:
                base,loc = info.django_code.split('-')
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
            self.update_settings(LANGUAGE_CODE = self.get_default_language())
        #~ self.update_settings(LANGUAGE_CODE = self.languages[0].django_code)
                    

    def do_site_startup(self):
        """
        Called by :meth:`djangosite.Site.startup`.
        """
        super(Site,self).do_site_startup()
        
        from django.conf import settings
        from django.utils.translation import ugettext_lazy as _
        from north.dbutils import set_language
        
        def langtext(code):
            for k,v in settings.LANGUAGES:
                if k == code: return v
            # returns None if not found

        def _add_language(code,lazy_text):
            self.LANGUAGE_DICT[code] = lazy_text
            self.LANGUAGE_CHOICES.append( (code,lazy_text) )

        #~ _add_language(DEFAULT_LANGUAGE,_(langtext(settings.LANGUAGE_CODE)))
        
        
        if self.languages is None:
          
            _add_language(DJANGO_DEFAULT_LANGUAGE,_("English"))
            
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
                            lang.django_code,[x[0] for x in settings.LANGUAGES]))
                        #~ return "English"
              
                text = _(text)
                _add_language(lang.django_code,text)
                
            """
            Activate the site's default language
            """
            set_language(self.get_default_language())

    def get_language_info(self,code):
        """
        Use this in Python fixtures or tests to test whether a 
        Site instance supports a given language. 
        `code` must be a Django-style language code
        If that specified language
        
        On a site with only one locale of a language (and optionally 
        some other languages), you can use only the language code to 
        get a tuple of `(django_code, babel_locale)`:
        
        >>> from north import TestSite as Site
        >>> Site(languages="en-us fr de-be de").get_language_info('en')
        LanguageInfo(django_code='en-us', name='en_US', index=0, suffix='')
        
        
        On a site with two locales of a same language (e.g. 'en-us' and 'en-gb'), 
        the simple code 'en' yields that first variant:
        
        >>> site = Site(languages="en-us en-gb")
        >>> print site.get_language_info('en')
        LanguageInfo(django_code='en-us', name='en_US', index=0, suffix='')
        
        """
        return self.language_dict.get(code,None)
        
    #~ def default_language(self):
        #~ """
        #~ Returns the default language of this website
        #~ as defined by :setting:`LANGUAGE_CODE` in your :xfile:`settings.py`.
        #~ """
        #~ return self.DEFAULT_LANGUAGE
        
    def resolve_languages(self,languages):
        """
        This is used by `UserProfile`.
        
        Examples:
        >>> from north import TestSite as Site
        >>> lst = Site(languages="en fr de nl et pt").resolve_languages('en fr')
        >>> [i.django_code for i in lst]
        ['en', 'fr']
        
        You may not specify languages which don't exist on this site:
        >>> Site(languages="en fr de").resolve_languages('en nl')
        Traceback (most recent call last):
          ...
        Exception: Unknown language code 'nl' (must be one of ['en', 'fr', 'de'])
        
        
        """
        rv = []
        if isinstance(languages,basestring):
            languages = languages.split()
        for k in languages:
            if isinstance(k,basestring):
                li = self.get_language_info(k)
                if li is None:
                    raise Exception("Unknown language code %r (must be one of %s)" % (
                        k,[li.name for li in self.languages]))
                rv.append(li)
            else:
                assert k in self.languages
                rv.append(k)
        return tuple(rv)
                
    def language_choices(self,language,choices):
        l = choices.get(language,None)
        if l is None:
            l = choices.get(self.DEFAULT_LANGUAGE)
        return l
        
    def get_default_language(self):
        """
        The default language to use in every `north.dbutils.LanguageField`.
        """
        return self.DEFAULT_LANGUAGE.django_code
        
    

    def babelkw(self,name,**kw):
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
        #~ d = { name : kw.get(default_language())}
        d = dict()
        #~ v = kw.get(self.DEFAULT_LANGUAGE)
        #~ if v is not None:
            #~ d[name] = v
        for simple,info in self.language_dict.items():
            # info = LanguageInfo()
            v = kw.get(simple,None)
            if v is not None:
                d[name+info.suffix] = v
                #~ if info.index == 0:
                    #~ d[name] = v
                #~ else:
                    #~ d[name+'_'+info.name] = v                  
        #~ for lang in self.BABEL_LANGS:
            #~ v = kw.get(lang,None)
            #~ if v is not None:
                #~ d[name+'_'+lang] = v
        return d
        
    def args2kw(self,name,*args):
        """
        Takes the basename of a BabelField and the values for each language.
        Returns a `dict` mapping the actual fieldnames to their values.
        """
        assert len(args) == len(self.languages)
        kw = {name:args[0]}
        for i,lang in enumerate(self.BABEL_LANGS):
            kw[name+'_'+lang] = args[i+1]
        return kw
            

    def field2kw(self,obj,name,**known_values):
        """
        Examples:
        
        >>> from north import TestSite as Site
        >>> from north.dbutils import set_language
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
        
        
        """
        #~ d = { self.DEFAULT_LANGUAGE.name : getattr(obj,name) }
        for lng in self.languages:
            v = getattr(obj,name+lng.suffix)
            if v:
                known_values[lng.name] = v
        return known_values
        
    def unused_field2kw(self,obj,name):
        """
        """
        d = { self.DEFAULT_LANGUAGE.name : getattr(obj,name) }
        for lang in self.BABEL_LANGS:
            v = getattr(obj,name+lang.suffix)
            if v:
                d[lang.name] = v
        return d
      
    def field2args(self,obj,name):
        """
        Return a list of the babel values of this field in the order of
        this Site's :attr:`Site.languages` attribute.
        
        """
        return [getattr(obj,name+li.suffix) for li in self.languages]
        #~ l = [ getattr(obj,name) ]
        #~ for lang in self.BABEL_LANGS:
            #~ l.append(getattr(obj,name+'_'+lang))
        #~ return l
      

    def babelitem(self,**v):
        """
        Given a dictionary with babel values, return the 
        value corresponding to the current language.
        This is available in templates as a function `tr`.
        
        >>> kw = dict(de="Hallo",en="Hello",fr="Salut")
        
        >>> from north import TestSite as Site
        >>> from north.dbutils import set_language
        >>> site = Site(languages="de en")
        >>> tr = site.babelitem
        >>> set_language('de')
        >>> tr(**kw)
        'Hallo'
        
        >>> set_language('en')
        >>> tr(**kw)
        'Hello'
        
        >>> set_language('jp')
        >>> tr(**kw)
        'Hallo'
        
        >>> 
        """
        from django.utils import translation
        info = self.language_dict.get(translation.get_language(),self.DEFAULT_LANGUAGE)
        #~ lng = translation.get_language()
        #~ print lng,v
        #~ lng = LANG or DEFAULT_LANGUAGE
        if info == self.DEFAULT_LANGUAGE:
            return v.get(info.name)
        x = v.get(info.name,None)
        if x is None:
            return v.get(self.DEFAULT_LANGUAGE.name)
        return x
        
    # babel_get(v) = babelitem(**v)
            
    def babeldict_getitem(self,d,k):
        v = d.get(k,None)
        if v is not None:
            assert type(v) is dict
            return self.babelitem(**v)
            
        
    def babelattr(self,obj,attrname,default=NOT_PROVIDED,language=None):
        """
        Return the value of the specified babel field `attrname` of `obj`
        in the current language.
        
        This is to be used in multilingual document templates.
        For example in a document template of a Contract you may use the following expression::

          babelattr(self.type,'name')

        This will return the correct value for the current language.
        
        Examples:
        
        >>> from north import TestSite as Site
        >>> from north.dbutils import set_language
        >>> from atelier.utils import AttrDict
        >>> def testit(site_languages):
        ...     site = Site(languages=site_languages)
        ...     obj = AttrDict(site.babelkw('name',de="Hallo",en="Hello",fr="Salut"))
        ...     return site,obj
        
        
        >>> site,obj = testit('de en')
        >>> set_language('de')
        >>> site.babelattr(obj,'name')
        'Hallo'
        
        >>> set_language('en')
        >>> site.babelattr(obj,'name')
        'Hello'
        
        If the object has no translation for a given language, 
        return the site's default language.
        Two possible cases:
        The language exists on the site, but the object has no translation for it:
        
        >>> site,obj = testit('en es')
        >>> set_language('es')
        >>> site.babelattr(obj,'name')
        'Hello'
        
        Or a language has been activated which doesn't exist on the site:
       
        >>> set_language('fr')
        >>> site.babelattr(obj,'name')
        'Hello'
        
        """
        if language is None:
            from django.utils import translation
            language = translation.get_language()
        info = self.language_dict.get(language,self.DEFAULT_LANGUAGE)
        if info.index != 0:
            v = getattr(obj,attrname+info.suffix,None)
            if v: 
                return v
        if default is NOT_PROVIDED:
            return getattr(obj,attrname)
        else:
            return getattr(obj,attrname,default)
        #~ if lang is not None and lang != self.DEFAULT_LANGUAGE:
            #~ v = getattr(obj,attrname+"_"+lang,None)
            #~ if v:
                #~ return v
        #~ return getattr(obj,attrname,*args)
            

class TestSite(Site):
    """
    Used to simplify doctest strings because it inserts default 
    values for the two first arguments that are mandatory but 
    not used in our examples::
    
    >> from north import Site
    >> Site(__file__,{},...)
    
    >> from north import TestSite as Site
    >> Site(...)
    
    
    
    """
    def __init__(self,*args,**kwargs):
        kwargs.update(no_local=True)
        g = dict(__file__=__file__)
        super(TestSite,self).__init__(g,*args,**kwargs)
        
    #~ def run_djangosite_local(self):
        #~ pass
        

