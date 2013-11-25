# -*- coding: UTF-8 -*-
# Copyright 2013 by Luc Saffre.
# License: BSD, see LICENSE for more details.

"""

"""

from __future__ import unicode_literals

#~ import logging
#~ logger = logging.getLogger(__name__)

import collections
LanguageInfo = collections.namedtuple(
    'LanguageInfo', ('django_code', 'name', 'index', 'suffix'))


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
        if len(language[p + 1:]) > 2:
            return language[:p].lower() + '_' + language[p + 1].upper() + language[p + 2:].lower()
        return language[:p].lower() + '_' + language[p + 1:].upper()
    else:
        return language.lower()


class Cycler:

    """
    Turns a list of items into an endless loop.
    Useful when generating demo fixtures.
    
    >>> from north.utils import Cycler
    >>> def myfunc():
    ...     yield "a"
    ...     yield "b"
    ...     yield "c"
    
    >>> c = Cycler(myfunc())
    >>> s = ""
    >>> for i in range(10):
    ...     s += c.pop()
    >>> print s
    abcabcabca
    
    An empty Cycler or a Cycler on an empty list will endlessly pop None values:
    
    >>> c = Cycler()
    >>> print c.pop(), c.pop(), c.pop()
    None None None
    
    >>> c = Cycler([])
    >>> print c.pop(), c.pop(), c.pop()
    None None None
    
    """

    def __init__(self, *args):
        """
        If there is exactly one argument, then this must be an iterable
        and will be used as the list of items to cycle on.
        If there is more than one positional argument, then these 
        arguments themselves will be the list of items.
        """

        if len(args) == 0:
            self.items = []
        elif len(args) == 1:
            self.items = list(args[0])
        else:
            self.items = args
        self.current = 0

    def pop(self):
        if len(self.items) == 0:
            return None
        item = self.items[self.current]
        self.current += 1
        if self.current >= len(self.items):
            self.current = 0
        if isinstance(item, Cycler):
            return item.pop()
        return item

    def __len__(self):
        return len(self.items)

    def reset(self):
        self.current = 0


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
