import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'pyramid',
    'zope.interface',
    'pyScss',
    ]

setup(name='pyramid_scss',
      version='0.0',
      description='pyramid-scss',
      long_description="",
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Jesse Dhillon',
      author_email='jesse@deva0.net',
      url='',
      keywords='web wsgi scss pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires = requires,
      )
