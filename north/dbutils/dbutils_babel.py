# -*- coding: UTF-8 -*-
# Copyright 2009-2014 by Luc Saffre.
# License: BSD, see LICENSE for more details.

from django.utils import translation


def run_with_language(lang, func):
    """Selects the specified language `lang`, calls the specified
    function `func`, restores the previously selected language.
    
    Deprecated: use translation.override() instead of this.

    """
    with translation.override(lang):
        return func()


