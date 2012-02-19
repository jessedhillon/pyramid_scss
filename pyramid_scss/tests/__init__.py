import os
import csv

from unittest import TestCase
from pyramid import testing
from pyramid.asset import abspath_from_asset_spec

import pyramid_scss

class PyramidScssTestCase(TestCase):
    scss_settings = {
        'scss.asset_path': 'pyramid_scss.tests:fixtures',
        'scss.caching': True,
    }

    def setUp(self):
        self.config = testing.setUp(settings=self.scss_settings)
        pyramid_scss.includeme(self.config)

        self._load_fixtures()

    def _load_fixtures(self):
        self.fixtures = {}
        fixture_path = abspath_from_asset_spec('pyramid_scss.tests:fixtures')
        for path, dirs, files in os.walk(fixture_path):
            for name in files:
                with open(os.path.join(path, name)) as f:
                    key = ''.join(name.split('.')[:-1])
                    self.fixtures.setdefault(key, f.read())


class DummyRequest(object):
    def __init__(self):
        self.matchdict = {}
