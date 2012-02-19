import string
import random

from pyramid_scss.tests import PyramidScssTestCase, DummyRequest
import pyramid_scss.controller as controller

class CacheTestCase(PyramidScssTestCase):
    @staticmethod
    def generate_id(count):
        return ''.join(random.choice(string.ascii_uppercase + string.lowercase + string.digits) for i in range(count))

    def test_cache(self):
        self.renderer.options.update({
            'cache': True
        })

        request = DummyRequest(self.config.registry)
        request.matchdict.update({
            'css_path': 'test'
        })

        response = self.renderer(self.fixtures.get('test.scss'), {'request': request})

        random_id = CacheTestCase.generate_id(8)
        modified = self.fixtures.get('test.scss') + '\n#{id} {{color: black}}'.format(id=random_id)
        new_response = self.renderer(modified, {'request': request})

        assert response == new_response
        assert random_id not in new_response

    def test_nocache(self):
        self.renderer.options.update({
            'cache': False
        })

        request = DummyRequest(self.config.registry)
        request.matchdict.update({
            'css_path': 'test'
        })

        response = self.renderer(self.fixtures.get('test.scss'), {'request': request})

        random_id = CacheTestCase.generate_id(8)
        modified = self.fixtures.get('test.scss') + '\n#{id} {{color: black}}'.format(id=random_id)
        new_response = self.renderer(modified, {'request': request})

        assert response != new_response
        assert random_id in new_response
