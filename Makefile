.PHONY: mm cm makedocs tests sdist

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  mm     run django-admin makemessages on modlib"
	@echo "  cm     run django-admin compilemessages on modlib"
	@echo "  tests  run Lino test suite"

sdist:
	python setup.py sdist --formats=gztar --dist-dir=docs/dl 
	#~ python setup.py register sdist --formats=gztar,zip upload 
	#~ python setup.py sdist --formats=gztar,zip --dist-dir=docs/dist
  
upload:
	python setup.py sdist --formats=gztar --dist-dir=docs/dl upload 
