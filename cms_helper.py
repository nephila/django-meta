#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

HELPER_SETTINGS = dict(
    ROOT_URLCONF='tests.example_app.urls',
    INSTALLED_APPS=[
        'meta',
        'tests.example_app',
    ],
    META_SITE_PROTOCOL='http',
    META_USE_SITES=True,
    META_USE_OG_PROPERTIES=True,
    META_USE_TWITTER_PROPERTIES=True,
    META_USE_GOOGLEPLUS_PROPERTIES=True,
)

try:
    import sekizai  # NOQA

    HELPER_SETTINGS['INSTALLED_APPS'].append('sekizai')
    HELPER_SETTINGS['TEMPLATE_CONTEXT_PROCESSORS'] = [
        'sekizai.context_processors.sekizai',
    ]
except ImportError:
    pass


def run():
    from djangocms_helper import runner
    runner.run('meta')


def setup():
    import sys
    from djangocms_helper import runner
    runner.setup('meta', sys.modules[__name__])

if __name__ == '__main__':
    run()
