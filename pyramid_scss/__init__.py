import os

from zope.interface import implements
from zope.interface import Interface

from pyramid.interfaces import ITemplateRenderer
from pyramid.exceptions import ConfigurationError
from pyramid.resource import abspath_from_resource_spec, abspath_from_asset_spec

from scss import Scss

def asbool(v):
    if isinstance(v, (str, unicode)):
        v = v.strip().lower()
        if v in ['true', 'yes', 'on', 'y', 't', '1']:
            return True
        elif v in ['false', 'no', 'off', 'n', 'f', '0']:
            return False
        else:
            raise ValueError("String is not true/false: {0}".format(v))
    return bool(v)

def renderer_factory(info):
    settings = info.settings

    options = {
        'compress': settings.get('scss.compress', False),
        'cache': settings.get('scss.cache', False),
        'comments': settings.get('scss.comments', True),
        'sort': settings.get('scss.sort', True),
        'warn': settings.get('scss.warn', True),
    }

    for k, v in options.items():
        options[k] = asbool(v)

    directories = settings.get('scss.path', None)

    if directories is None:
        raise ConfigurationError('SCSS renderer used without ``scss.path`` setting')
    if isinstance(directories, basestring):
        directories = filter(None, [d.strip() for d in directories.splitlines()])
    options['path'] = [abspath_from_resource_spec(d) for d in directories]

    return ScssRenderer(info, options)

class ScssRenderer(object):
    implements(ITemplateRenderer)
    cache = None

    def __init__(self, info, options):
        self.cache = {}
        self.info = info
        self.template_path = abspath_from_asset_spec(info.settings.get('scss.path', False))

    def __call__(self, scss, system):
        parser = Scss()

        if 'request' in system:
            request = system['request']
            request.response_content_type = 'text/css'

            if scss in self.cache:
                return self.cache[scss]
            self.cache[scss] = parser.compile(scss)
            return self.cache[scss]

        return parser.compile(scss)

def includeme(config):
    config.add_renderer('scss', renderer_factory)
