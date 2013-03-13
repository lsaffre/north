"""

"""

import os

from djangosite import Site
#~ from north.babel import BabelSiteMixin
#~ from north.babel import Site

#~ execfile(os.path.join(os.path.dirname(__file__),'version.py'))
execfile(os.path.join(os.path.dirname(__file__),'setup_info.py'))
#~ execfile(os.path.join(os.path.dirname(__file__),'..','setup_info.py'))

__version__ = SETUP_INFO['version'] # 


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


LANGUAGE_CODE_MAX_LENGTH = 2
"""
"""

def simplified_code(code):
    """
    We store only the main code, supposing that nobody maintains
    multilingual database content for different variants of the 
    same language.
    """
    return code[:LANGUAGE_CODE_MAX_LENGTH].strip()

#~ DEFAULT_LANGUAGE = simplified_code(settings.LANGUAGE_CODE)


class Site(Site):
    """
    Extends :class:`djangosite.Site`
    by adding some attributes and methods used by `north`.
    """
    
    demo_fixtures = ['std','demo']
    """
    The list of fixtures to be loaded by the 
    `initdb_demo <lino.management.commands.initdb_demo>`
    command.
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
    See also :doc:`/blog/2011/0901`.
    """
    
    #~ def __init__(self,*args):
    def init_nolocal(self,*args):
        super(Site,self).init_nolocal(*args)
        self.update_settings(SERIALIZATION_MODULES = {
            "py" : "north.dpy",
        })
        
        
    def install_migrations(self,*args):
        """
        See :func:`lino.utils.dumpy.install_migrations`.
        """
        from .dpy import install_migrations
        install_migrations(self,*args)
        
          
    def using(self,ui=None):
        for u in super(Site,self).using(ui): yield u
        yield (SETUP_INFO['name'],SETUP_INFO['version'],SETUP_INFO['url'])
        
   
    def apply_languages(self):
      
        super(Site,self).apply_languages()
      
        self.LANGUAGE_CHOICES = []
        self.LANGUAGE_DICT = dict() # used in lino.modlib.users
        
        if self.languages is None:
            self.DEFAULT_LANGUAGE = 'en'
            self.AVAILABLE_LANGUAGES = (self.DEFAULT_LANGUAGE,)
            self.BABEL_LANGS = tuple()
        else:
            self.DEFAULT_LANGUAGE = self.languages[0]
            self.BABEL_LANGS = tuple(self.languages[1:])
            self.AVAILABLE_LANGUAGES = (self.DEFAULT_LANGUAGE,) + self.BABEL_LANGS
          

    def do_site_startup(self):
      
        super(Site,self).do_site_startup()
        
        from django.conf import settings
        
        def langtext(code):
            for k,v in settings.LANGUAGES:
                if k == code: return v
            raise Exception(
                "Unknown language code %r (must be one of %s)" % (
                code,[x[0] for x in settings.LANGUAGES]))
            #~ return "English"

        def _add_language(code,text,full_code):
            self.LANGUAGE_DICT[code] = text
            self.LANGUAGE_CHOICES.append( (code,text) )

        #~ _add_language(DEFAULT_LANGUAGE,_(langtext(settings.LANGUAGE_CODE)))
        
        from django.utils.translation import ugettext_lazy as _
      
        if self.languages is None:
          
            _add_language('en',_("English"),'en-us')
            
        else:
          
            for code in self.languages:
                text = _(langtext(code))
                k = simplified_code(code)
                if k in self.LANGUAGE_DICT:
                    raise Exception("Duplicate base language %r" % k)
                _add_language(k,text,code)
                

            #~ LANGUAGE_CHOICES = [ (k,_(v)) for k,v in settings.LANGUAGES 
                  #~ if k in settings.SITE.languages]

            #~ assert self.DEFAULT_LANGUAGE in [x[0] for x in self.django_settings.LANGUAGES]
          
            #~ self.BABEL_LANGS = [x[0] for x in self.LANGUAGE_CHOICES if x[0] != self.DEFAULT_LANGUAGE]
            #~ BABEL_LANGS = [x[0] for x in settings.LANGUAGES if x[0] != DEFAULT_LANGUAGE]
          

        #~ self.BABEL_LANGS = tuple(self.BABEL_LANGS)

        #~ logger.info("20130311 Languages: %s ",AVAILABLE_LANGUAGES)

    def default_language(self):
        """
        Returns the default language of this website
        as defined by :setting:`LANGUAGE_CODE` in your :xfile:`settings.py`.
        """
        return self.DEFAULT_LANGUAGE
        
        
    def language_choices(self,language,choices):
        l = choices.get(language,None)
        if l is None:
            l = choices.get(self.DEFAULT_LANGUAGE)
        return l


