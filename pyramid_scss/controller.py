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
    for s in request.registry.settings.get('scss.asset_path').split('\n'):
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
    def __init__(self, *args, **kwargs):
        kwargs['use_subpath'] = True
        self.static_view = static_view(*args, **kwargs)

    def __call__(self, context, request):
        try:
            render = get_renderer('scss')
            system = dict(request=request)
            return Response(render(get_scss(context, request), system),
                            content_type='text/css',
                            status='200 OK')
        except HTTPNotFound:
            return self.static_view(context, request)
