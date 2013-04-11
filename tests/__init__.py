from unipath import Path

ROOTDIR = Path(__file__).parent.parent

# load  SETUP_INFO:
execfile(ROOTDIR.child('north','setup_info.py'),globals())

from atelier.test import SubProcessTestCase

class BaseTestCase(SubProcessTestCase):
    default_environ = dict(DJANGO_SETTINGS_MODULE="lino.projects.std.settings")
    project_root = ROOTDIR
    
class BasicTests(BaseTestCase):
    def test_z01(self): 
        self.assertEqual(1+1,2)

    def test_init(self): self.run_simple_doctests('north/__init__.py')
    def test_utils(self): self.run_simple_doctests('north/utils.py')
    def test_catalog(self): self.run_docs_django_tests('tutorials.catalog.settings')
    def test_polls(self): self.run_django_manage_test('docs/tutorials/polls')

class PackagesTests(BaseTestCase):
    def test_packages(self): self.run_packages_test(SETUP_INFO['packages'])


#~ env.django_doctests.append('tutorials.catalog.settings')

# invoke only these with ``fab t4``:
#~ env.simple_doctests.append('north/__init__.py')

# invoke only these with ``fab t7``:
#~ env.bash_tests.append('python docs/tutorials/polls/manage.py test polls')

# invoke only these with ``fab t5``:
#~ env.django_databases.append('docs/tutorials/polls')

