import os
import csv
from collections import namedtuple

from unittest import TestCase
from pyramid import testing
from pyramid.asset import abspath_from_asset_spec
from pyramid.renderers import get_renderer

import pyramid_scss

class PyramidScssTestCase(TestCase):
    scss_settings = {
        'scss.asset_path': """
            pyramid_scss.tests:fixtures
            pyramid_scss.tests:fixtures/resources
        """,
        'scss.static_path': 'pyramid_scss.tests:fixtures/static',
        'scss.static_url_root': '/static/',
        'scss.output_path': 'pyramid_scss.tests:fixtures/compiled',
        'scss.output_url_root': '/compiled/',
        'scss.cache': True,
    }

    def setUp(self):
        self.config = testing.setUp(settings=self.scss_settings)
        pyramid_scss.includeme(self.config)
        self.renderer = get_renderer('scss')

        self._load_fixtures()

    def _load_fixtures(self):
        self.fixtures = {}
        fixture_path = abspath_from_asset_spec('pyramid_scss.tests:fixtures')
        for path, dirs, files in os.walk(fixture_path):
            for name in files:
                if name.endswith('.png'):
                    mode = 'rb'
                else:
                    mode = 'r'
                with open(os.path.join(path, name), mode) as f:
                    self.fixtures.setdefault(name, f.read())


class DummyRequest(object):
    def __init__(self, registry):
        self.registry = registry
        self.matchdict = {}
        self.subpath = ()
        self.response = namedtuple('Response', ['content_type'])
