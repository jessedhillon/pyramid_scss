import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
readme = open(os.path.join(here, 'README.rst'), 'r').read()
changes = open(os.path.join(here, 'CHANGES.rst'), 'r').read()

requires = [
    'pyramid',
    'zope.interface',
    'pyScss',
]

setup(
    name='pyramid_scss',
    version='0.1.1',
    description="Adds support for SCSS to Pyramid projects",
    long_description="{0}\n\n{1}".format(readme, changes),
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Software Development :: Code Generators",
    ],
    author='Jesse Dhillon',
    author_email='jesse@deva0.net',
    url='https://github.com/jessedhillon/pyramid_scss',
    keywords='web wsgi css scss pyramid',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires = requires,
)
