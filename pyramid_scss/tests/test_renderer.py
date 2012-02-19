from pyramid_scss.tests import PyramidScssTestCase, DummyRequest
import pyramid_scss.controller as controller

class RendererTestCase(PyramidScssTestCase):
    def test_nocompress(self):
        self.renderer.options.update({
            'compress': False
        })

        request = DummyRequest(self.config.registry)
        request.matchdict.update({
            'css_path': 'test'
        })

        rendered = self.renderer(self.fixtures.get('test.scss'), {'request': request})
        assert rendered == self.fixtures.get('test_nocompress.css')

    def test_compress(self):
        self.renderer.options.update({
            'compress': True
        })

        request = DummyRequest(self.config.registry)
        request.matchdict.update({
            'css_path': 'test'
        })

        rendered = self.renderer(self.fixtures.get('test.scss'), {'request': request})
        assert rendered == self.fixtures.get('test_compress.css')

    def test_import(self):
        request = DummyRequest(self.config.registry)
        request.matchdict.update({
            'css_path': 'import'
        })

        rendered = self.renderer(self.fixtures.get('import.scss'), {'request': request})
        assert '#imported_resource' in rendered
