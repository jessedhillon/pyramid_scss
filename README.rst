============
pyramid_scss
============

Overview
============
This module provides a convenient bit of glue code around `pyScss <https://github.com/Kronuz/pyScss>`_, allowing your Pyramid projects to use stylesheets authored in `SCSS <http://sass-lang.com/docs/yardoc/file.SCSS_FOR_SASS_USERS.html>`_. 

Installation
============
Install using setuptools, e.g. (within a virtualenv)::

    $ pip install pyramid_scss

Or if you prefer to get the latest from Github::

    $ git clone git://github.com/jessedhillon/pyramid_scss.git

Configuration
===============
The only setting which is necessary is ``asset_path`` which is an asset spec which points to the root folder where your SCSS stylesheets are. An easy way to set that is to add this line to the ``[app:main]`` section of your ``project.ini``::

    scss.asset_path = myproject:assets/scss

``asset_path`` can be a newline delimited string of multiple asset paths. Each path will be searched, in order, until the matching stylesheet is found. An unmatched request will raise ``pyramid.httpexceptions.HTTPNotFound``.

``static_path`` is a path to the static assets necessary to construct a stylesheet. Unlike ``asset_path``, this setting only accepts one path. ``static_url_root`` is required if you set ``static_path``, and it serves as a path prefix when generating the URL for a static resource.

``output_path`` is the path where generated assets will be output, such as spritemaps. Also, ``output_url_root`` is a required setting if ``output_path`` is provided, and will be prefix the path component of the URL generated in reference to compiled resources.

There are a couple of other options. ``compress`` controls whether or not the output documents are compressed (all whitespace stripped)::

    scss.compress = false

The other option is ``cache``, which will store both the contents of the file and the rendered output in memory::

    scss.cache = true

Usage
===============
First, use ``config.include`` to initialize the extension::

    config.include("pyramid_scss")

Second, assuming you are using URL dispatch, add a route to serve css::

    config.add_route('css', '/css/{css_path:.*}.css')
    config.add_view(route_name='css', view='pyramid_scss.controller.get_scss', renderer='scss', request_method='GET')

Alternatively, you can configure ``pyramid_scss`` to shadow a path which already contains static assets, and default to a ``static_view`` if no SCSS stylesheet matches the request. In your ``project.ini``::

    scss.static_route =
        css = project:assets/css/

With this configuration, a request for ``/css/style.css`` will first look for ``style.scss`` in ``scss.asset_path`` and if it's not found, then a ``static_view`` for ``project:assets/css/`` will be consulted. If you have this configuration, then you can generate a route for a static asset with ``static_url`` and those requests will transparently map to SCSS stylesheets.

*TODO:* Add a traversal example.

In the example above, an SCSS stylesheet located at ``myproject/assets/scss/style.scss`` (using the ``asset_path`` configured in the Configuration section) could be accessed by a URL request to ``http://myproject/css/style.css``. This route would also resolve stylesheets in subdirectories of ``asset_path``.
