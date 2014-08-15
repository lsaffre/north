# pro-forma settings file.
from north import Site
#~ SITE = Site(__file__,globals(),no_local=True)
SITE = Site(globals(),no_local=True)
SECRET_KEY = "20227" # see :djangoticket:`20227`
