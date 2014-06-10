from setuptools import setup
#~ from distutils.core import setup
execfile('north/project_info.py')
if __name__ == '__main__':
    setup(**SETUP_INFO)
