#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

HELPER_SETTINGS = dict(
    ROOT_URLCONF='example_app.urls',
    INSTALLED_APPS=[
        'sekizai',
        'meta',
        'example_app',
    ],
    META_SITE='http://foo.com',
    META_SITE_PROTOCOL='http',
    META_USE_SITES=True,
    META_USE_OG_PROPERTIES=True,
    META_USE_TWITTER_PROPERTIES=True,
    META_USE_GOOGLEPLUS_PROPERTIES=True,
    NOSE_ARGS=['-s'],
    TEMPLATE_CONTEXT_PROCESSORS=[
        'sekizai.context_processors.sekizai',
    ],
)


def run():
    from djangocms_helper import runner
    runner.run('meta')


if __name__ == '__main__':
    run()
