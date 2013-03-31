# -*- coding: UTF-8 -*-
"""
:copyright: Copyright 2013 by Luc Saffre.
:license: BSD, see LICENSE for more details.

"""

from __future__ import unicode_literals

#~ import logging
#~ logger = logging.getLogger(__name__)

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
    
    A Cycler on an empty list will endlessly pop None values:
    
    >>> c = Cycler([])
    >>> print c.pop(), c.pop(), c.pop()
    None None None
    
    """
    def __init__(self,*args):
        if len(args) == 0:
            raise ValueError()
        elif len(args) == 1:
            self.items = list(args[0])
        else:
            self.items = args
        self.current = 0
        
    def pop(self):
        if len(self.items) == 0: return None
        item = self.items[self.current]
        self.current += 1
        if self.current >= len(self.items):
            self.current = 0
        if isinstance(item,Cycler):
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

