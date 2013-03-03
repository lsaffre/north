DJANGO_ADMIN=python $(shell python -c "from os.path import join,dirname; from django import bin;print join(dirname(bin.__file__),'django-admin.py')")
DJANGO_ADMIN := $(shell cygpath -m $(DJANGO_ADMIN))
SITENAME               = north
TEMPDIR                = C:\\temp\\sphinxbuild\\$(SITENAME)
#~ TEMPDIR                = /cygdrive/c/temp/sphinxbuild/$(SITENAME)
BUILDDIR               = $(TEMPDIR)\\html
CACHEDIR               = $(TEMPDIR)\\doctrees
#~ AUTODOC                = python l:\\snapshots\\sphinx-autopackage-script\\generate_modules.py
#~ LINO_SRC     = t:\\hgwork\\lino\\lino
# LINO_SRC     = `python -c "import lino,os; print os.path.dirname(lino.__file__)"`


# You can set these variables from the command line.
SPHINXOPTS = -w warnings.txt -n -P 
#~ SPHINXOPTS    = -w warnings.txt -n -P -D keep_warnings=True
#~ SPHINXOPTS    = -W 
#~ SPHINXOPTS    = 
#~ SPHINXBUILD   = python l:\\snapshots\\sphinx\\sphinx-build.py
SPHINXBUILD   = sphinx-build
PAPER         =

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = $(PAPEROPT_$(PAPER)) $(SPHINXOPTS)


.PHONY: help clean html show web pickle htmlhelp latex changes linkcheck makedocs

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html      to make standalone HTML files"
	@echo "  pickle    to make pickle files"
	@echo "  json      to make JSON files"
	@echo "  htmlhelp  to make HTML files and a HTML help project"
	@echo "  latex     to make LaTeX files, you can set PAPER=a4 or PAPER=letter"
	@echo "  changes   to make an overview over all changed/added/deprecated items"
	@echo "  linkcheck to check all external links for integrity"

clean:
	-rm -rf $(CACHEDIR)
	-rm -rf $(BUILDDIR)

html:
	mkdir -p $(CACHEDIR) 
	mkdir -p $(BUILDDIR)
	$(SPHINXBUILD) -b html -d $(CACHEDIR) $(ALLSPHINXOPTS) . $(BUILDDIR)
	cp -ru dl $(TEMPDIR)\\html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)."

  
upload:
	cd $(BUILDDIR) && rsync -r --progress --delete --times ./ luc@lino-framework.org:~/public_html/$(SITENAME)
	#python ../setup.py upload_sphinx --upload-dir $(BUILDDIR)
	#cd $(BUILDDIR) && rsync -r --progress --delete --times ./ luc@saffre-rumma.net:~/public_html/sphinxbuild/$(SITENAME)


doctest:
	mkdir -p $(CACHEDIR) 
	mkdir -p $(BUILDDIR)
	$(SPHINXBUILD) -b doctest -d $(CACHEDIR) $(ALLSPHINXOPTS) . $(BUILDDIR)
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)."

unused_html:        
	set DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS_MODULE); $(SPHINXBUILD) -b html -d $(CACHEDIR) $(ALLSPHINXOPTS) . $(BUILDDIR)


pickle:
	mkdir -p .build/pickle .build/doctrees
	$(SPHINXBUILD) -b pickle $(ALLSPHINXOPTS) .build/pickle
	@echo
	@echo "Build finished; now you can process the pickle files."

web: pickle

json:
	mkdir -p .build/json .build/doctrees
	$(SPHINXBUILD) -b json $(ALLSPHINXOPTS) .build/json
	@echo
	@echo "Build finished; now you can process the JSON files."

htmlhelp:
	mkdir -p .build/htmlhelp .build/doctrees
	$(SPHINXBUILD) -b htmlhelp $(ALLSPHINXOPTS) .build/htmlhelp
	@echo
	@echo "Build finished; now you can run HTML Help Workshop with the" \
	      ".hhp project file in .build/htmlhelp."

