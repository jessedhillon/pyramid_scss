import os
import logging

from pyramid.exceptions import ConfigurationError
from pyramid.httpexceptions import HTTPNotFound
from pyramid.resource import abspath_from_asset_spec

_Cache = {}
Logger = logging.getLogger('pyramid_scss')

def get_scss(root, request):
    Logger.info('serving SCSS request for %s', request.matchdict.get('css_path'))
    scss = _load_asset(request)

    if scss is None:
        raise HTTPNotFound()

    return scss

def _get_asset_path(request):
    if 'scss.asset_path' not in request.registry.settings:
        raise ConfigurationError('SCSS renderer requires ``scss.asset_path`` setting')

    filename = request.matchdict.get('css_path') + '.scss'
    paths = []
    for s in request.registry.settings.get('scss.asset_path').split('\n'):
        if s:
            p = abspath_from_asset_spec(os.path.join(s.strip(), filename))
            paths.append(p)

    return paths

def _load_asset(request):
    caching = request.registry.settings.get('scss.cache', False)
    paths = _get_asset_path(request)

    for p in paths:
        if caching and p in _Cache:
            return _Cache.get(p)

        if os.path.exists(p):
            _Cache[p] = open(p).read()
            return _Cache.get(p)

    return None
