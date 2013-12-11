from unipath import Path

ROOTDIR = Path(__file__).parent.parent

# load  SETUP_INFO:
execfile(ROOTDIR.child('north', 'project_info.py'), globals())

from djangosite.utils.pythontest import TestCase


class BaseTestCase(TestCase):
    demo_settings_module = "north.demo.settings"
    project_root = ROOTDIR


class BasicTests(BaseTestCase):

    def test_z01(self):
        self.assertEqual(1+1, 2)

    def test_site(self):
        self.run_simple_doctests('north/north_site.py')

    def test_utils(self):
        self.run_simple_doctests('north/utils.py')

    def test_dbutils(self):
        self.run_simple_doctests('north/dbutils.py')

    def test_catalog(self):
        self.run_docs_django_tests('tutorials.catalog.settings')

    def test_polls(self):
        self.run_django_manage_test('docs/tutorials/polls')


class PackagesTests(BaseTestCase):

    def test_packages(self):
        self.run_packages_test(SETUP_INFO['packages'])




