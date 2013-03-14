from djangosite.utils.fablib import *
setup_from_project("north")  

env.django_doctests.append('tutorials.catalog.settings')
#~ env.django_doctests.append('tutorials.polls.mysite.settings')

# t7
env.bash_tests.append('python docs/tutorials/polls/manage.py test polls')

#~ env.simple_doctests.append('djangosite/utils/__init__.py')
