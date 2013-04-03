from __future__ import absolute_import, unicode_literals

from django import template

register = template.Library()

@register.simple_tag
def og_prop(name, value):
    return '<meta property="og:%s" content="%s">' % (name, value)

@register.simple_tag
def meta(name, value):
    return '<meta name="%s" content="%s">' % (name, value)

@register.simple_tag
def meta_list(name, lst):
    try:
        return '<meta name="%s" content="%s">' % (name, ', '.join(lst))
    except:
        return ''
