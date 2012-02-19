import os
import logging

from zope.interface import implements
from zope.interface import Interface

from pyramid.interfaces import ITemplateRenderer
from pyramid.exceptions import ConfigurationError
from pyramid.resource import abspath_from_asset_spec

import scss
from scss import Scss

Logger = logging.getLogger('pyramid_scss')

def as_bool(s, default=False):
    if isinstance(s, bool):
        return s

    if isinstance(s, basestring):
        if s.lower() in ['true', 'yes', 'on', '1']:
            return True

        if s.lower() in ['false', 'no', 'off', '0']:
            return False

    return default

def prefixed_keys(d, prefix):
    return dict([(k.replace(prefix, ''), v) for k, v in d.items() if k.startswith(prefix)])

def _get_import_paths(settings):
    if 'scss.asset_path' not in settings:
        raise ConfigurationError('SCSS renderer requires ``scss.asset_path`` setting')

    load_paths = []
    for s in settings.get('scss.asset_path').split('\n'):
        if s:
            p = abspath_from_asset_spec(s.strip())
            load_paths.append(p)
            Logger.info('adding asset path %s', p)

    static_path = settings.get('scss.static_path', '')
    if static_path:
        static_path = abspath_from_asset_spec(static_path.strip())
        Logger.info('setting static path %s', static_path)

    return (load_paths, static_path)

def renderer_factory(info):
    settings = prefixed_keys(info.settings, 'scss.')

    options = {
        'compress': settings.get('compress', False),
        'cache': settings.get('cache', False),
    }

    options = dict((k, as_bool(v)) for k, v in options.items())
    return ScssRenderer(info, options)

class ScssRenderer(object):
    implements(ITemplateRenderer)
    cache = None

    def __init__(self, info, options):
        self.cache = {}
        self.info = info
        self.options = options

    def __call__(self, scss, system):
        parser = Scss(scss_opts=self.options)

        if 'request' in system:
            request = system.get('request')
            request.response_content_type = 'text/css'
            key = request.matchdict.get('css_path')

            if not self.options.get('cache', False) or key not in self.cache:
                Logger.info('generating %s', request.matchdict.get('css_path'))
                self.cache[key] = parser.compile(scss)

            return self.cache.get(key)

        return parser.compile(scss)

def includeme(config):
    load_paths, static_path = _get_import_paths(config.registry.settings)
    scss.LOAD_PATHS = ','.join([scss.LOAD_PATHS, ','.join(load_paths)])
    scss.STATIC_ROOT = static_path
    config.add_renderer('scss', renderer_factory)
