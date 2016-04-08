# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django import template


def addtoblock(parser, token):
    parser.parse(('endaddtoblock',))
    parser.delete_first_token()
    return StubNode()


class StubNode(template.Node):

    def render(self, context):
        return ''
