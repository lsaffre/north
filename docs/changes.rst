.. _north.changes: 

==================
Changes in `North`
==================

See the author's 
`Developer Blog <http://docs.lino-framework.org/blog>`_
to get detailed news.
The final truth about what's going on is the source code.


Version 0.1.4 (in development)
============================================

- Adapted test suite to changes in atelier and djangosite.
  Added :mod:`north.demo.settings` to remove depüendency from Lino.


Version 0.1.3 (released :blogref:`20130505`)
============================================

- When loading a dump which ended with a Warning "Abandoning with x 
  unsaved instances from ...", user got a traceback instead of the 
  warning.

Version 0.1.2 (released :blogref:`20130422`)
============================================

- Moved the set_language function from north to djangosite because 
  it is used in :mod:`djangosite.utils.sphinxconf`.

- Adapted copyright headers. 
  Replaced the `/releases` directory by a single file `/changes.rst`.
  See :blogref:`20130331`.

Version 0.1.1 (released 2013-03-29)
===================================

- Changes before 0.1.1 are not listed here.
  See the developers blog and/or the Mercurial log.

  This project was split out of 
  `Lino <https://pypi.python.org/pypi/lino>` in 
  March 2013.
  

