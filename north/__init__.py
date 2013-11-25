# Copyright 2013 by Luc Saffre.
# License: BSD, see LICENSE for more details.
"""
The top-level package of :ref:`north`.

"""

import os

execfile(os.path.join(os.path.dirname(__file__), 'project_info.py'))

__version__ = SETUP_INFO['version']

intersphinx_url = "http://north.lino-framework.org"

from .north_site import Site, TestSite
#~ from site import TestSite, LanguageInfo
