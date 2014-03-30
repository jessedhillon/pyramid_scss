import os
import logging

from zope.interface import implementer
from zope.interface import Interface

from pyramid.interfaces import ITemplateRenderer
from pyramid.exceptions import ConfigurationError
from pyramid.resource import abspath_from_asset_spec
from pyramid.settings import asbool

import scss
from scss import Scss

Logger = logging.getLogger('pyramid_scss')

__version__ = '0.4'

def prefixed_keys(d, prefix):
    return dict([(k.replace(prefix, ''), v) for k, v in d.items() if k.startswith(prefix)])

def _get_import_paths(settings):
    # `scss.asset_path` is the path which should be searched to resolve a request
    if 'scss.asset_path' not in settings:
        raise ConfigurationError('SCSS renderer requires ``scss.asset_path`` setting')

    load_paths = []
    for s in settings.get('scss.asset_path').split('\n'):
        if s:
            p = abspath_from_asset_spec(s.strip())
            load_paths.append(p)
            Logger.info('adding asset path %s', p)

    # `scss.static_path`, optional, is the path which should be searched to resolve references to static assets in stylesheets
    static_path = settings.get('scss.static_path', '')
    if static_path:
        if 'scss.static_url_root' not in settings:
            raise ConfigurationError('SCSS renderer requires ``scss.static_url_root`` setting if ``scss.static_path`` is provided')

        static_path = abspath_from_asset_spec(static_path.strip())
        Logger.info('setting static path %s', static_path)

    # `scss.output_path`, optional, is the path where generated spritemaps should be written
    assets_path = settings.get('scss.output_path', '')
    if assets_path:
        if 'scss.output_url_root' not in settings:
            raise ConfigurationError('SCSS renderer requires ``scss.output_url_root`` setting if ``scss.output_path`` is provided')

        assets_path = abspath_from_asset_spec(assets_path.strip())
        Logger.info('setting output path %s', assets_path)

    return (load_paths, static_path, assets_path)

def renderer_factory(info):
    settings = prefixed_keys(info.settings, 'scss.')

    options = {
        'compress': settings.get('compress', False),
        'cache': settings.get('cache', False),
    }

    options = dict((k, asbool(v)) for k, v in options.items())
    return ScssRenderer(info, options)

@implementer(ITemplateRenderer)
class ScssRenderer(object):
    cache = None

    def __init__(self, info, options):
        self.cache = {}
        self.info = info
        self.options = options

    def __call__(self, scss, system):
        parser = Scss(scss_opts=self.options)

        if 'request' in system:
            request = system.get('request')
            request.response.content_type = 'text/css'
            key = request.matchdict.get('css_path')

            if not self.options.get('cache', False) or key not in self.cache:
                Logger.info('generating %s', key)
                self.cache[key] = parser.compile(scss)

            return self.cache.get(key)

        return parser.compile(scss)

def includeme(config):
    load_paths, static_path, assets_path = _get_import_paths(config.registry.settings)

    scss.config.LOAD_PATHS = ','.join([scss.config.LOAD_PATHS, ','.join(load_paths)])

    scss.config.STATIC_ROOT = static_path
    scss.config.STATIC_URL = config.registry.settings.get('scss.static_url_root')

    scss.config.ASSETS_ROOT = assets_path
    scss.config.ASSETS_URL = config.registry.settings.get('scss.output_url_root')

    config.add_renderer('scss', renderer_factory)
