import os
import logging
from collections import Sequence

from pyramid.exceptions import ConfigurationError
from pyramid.httpexceptions import HTTPNotFound
from pyramid.renderers import get_renderer
from pyramid.response import Response
from pyramid.resource import abspath_from_asset_spec
from pyramid.static import static_view


Logger = logging.getLogger('pyramid_scss')


class SCSSController(object):
    def __init__(self, base_path):
        self.base_path = base_path.strip()

    def __call__(self, context, request):
        subpath = '/'.join(request.subpath)
        scss = self._load_asset(subpath)

        if scss is None:
            raise HTTPNotFound()

        Logger.info('serving SCSS request for %s', request.matchdict.get('css_path', request.subpath))
        return scss

    def _get_asset_path(self, css_path):
        if css_path.endswith('.css'):
            css_path = css_path.rsplit('.css')[0]

        filename = css_path + u'.scss'
        return abspath_from_asset_spec(os.path.join(self.base_path, filename))

    def _load_asset(self, path):
        path = self._get_asset_path(path)

        if os.path.exists(path):
            with open(path) as f:
                return f.read()

        return None


def get_scss(root, request):
    Logger.info('serving SCSS request for %s', request.matchdict.get('css_path'))
    scss = _load_asset(request)

    if scss is None:
        raise HTTPNotFound()

    return scss


def _get_asset_path(request):
    if 'scss.asset_path' not in request.registry.settings:
        raise ConfigurationError('SCSS renderer requires ``scss.asset_path`` setting')

    css_path = request.matchdict.get('css_path', request.subpath)

    if isinstance(css_path, Sequence) and not isinstance(css_path, basestring):
        css_path = u'/'.join(css_path)

    if css_path.endswith('.css'):
        css_path = css_path.rsplit('.css')[0]

    filename = css_path + u'.scss'
    paths = []
    for s in request.registry.settings.get('scss.asset_path').strip().splitlines():
        if s:
            p = abspath_from_asset_spec(os.path.join(s.strip(), filename))
            paths.append(p)

    return paths


def _load_asset(request):
    paths = _get_asset_path(request)

    for p in paths:
        if os.path.exists(p):
            with open(p) as f:
                return f.read()

    return None


class scss_static_view(object):
    def __init__(self, scss_spec, static_spec, *args, **kwargs):
        kwargs['use_subpath'] = True
        self.static_view = static_view(static_spec, *args, **kwargs)
        self.scss_view = SCSSController(scss_spec)

    def __call__(self, context, request):
        try:
            render = get_renderer('scss')
            system = dict(request=request)
            return Response(render(self.scss_view(context, request), system),
                            content_type='text/css', status='200 OK')
        except HTTPNotFound:
            return self.static_view(context, request)
