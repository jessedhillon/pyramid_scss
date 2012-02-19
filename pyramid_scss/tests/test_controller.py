from pyramid_scss.tests import PyramidScssTestCase, DummyRequest
import pyramid_scss.controller as controller

class ControllerTestCase(PyramidScssTestCase):
    def test_get_scss(self):
        request = DummyRequest(self.config.registry)
        request.matchdict.update({
            'css_path': 'test'
        })

        scss = controller.get_scss(None, request)
        assert self.fixtures.get('test.scss') == controller.get_scss(None, request)
