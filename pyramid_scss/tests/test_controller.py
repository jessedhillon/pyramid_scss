from pyramid.asset import abspath_from_asset_spec

from pyramid_scss.tests import PyramidScssTestCase, DummyRequest
import pyramid_scss.controller as controller

class ControllerTestCase(PyramidScssTestCase):
    def test_get_scss(self):
        request = DummyRequest()
        request.matchdict.update({
            'css_path': 'test'
        })

        scss = controller.get_scss(None, request)
        with open(abspath_from_asset_spec('pyramid_scss.tests:fixtures/test.scss')) as f:
            assert f.read() == scss
