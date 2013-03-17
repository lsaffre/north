from djangosite.utils.fablib import *
setup_from_project("north")  

env.django_doctests.append('tutorials.catalog.settings')
#~ env.django_doctests.append('tutorials.polls.mysite.settings')

# invoke only these with ``fab t4``:
env.simple_doctests.append('north/__init__.py')

# invoke only these with ``fab t7``:
#~ env.bash_tests.append('python docs/tutorials/polls/manage.py test polls')

# invoke only these with ``fab t5``:
env.django_databases.append('docs/tutorials/polls')

