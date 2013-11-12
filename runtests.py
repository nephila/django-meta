#!/usr/bin/env python

import sys
from os.path import dirname, abspath

from django.conf import settings, global_settings

from nose.plugins.plugintest import run_buffered as run

if not settings.configured:
    settings.configure(
        INSTALLED_APPS=[
            'meta',
        ],
        STATIC_URL='/static/',
        ROOT_URLCONF='',
        DEBUG=False,
        SITE_ID=1,
    )

def runtests(*test_args, **kwargs):
    if not test_args:
        test_args = ['tests']

    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)

    run(argv=sys.argv)

if __name__ == '__main__':
    runtests()

