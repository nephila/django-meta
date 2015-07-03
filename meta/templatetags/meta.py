from __future__ import absolute_import, unicode_literals

from django import template
from django.utils.html import escape

register = template.Library()


@register.simple_tag
def title_prop(value):
    return '<title>%s</title>' % escape(value)


@register.simple_tag
def generic_prop(namespace, name, value):
    """
    Generic property setter that allows to create custom namespaced meta
    """
    return custom_meta('property', '%s:%s' % (namespace, name), value)


@register.simple_tag
def og_prop(name, value):
    return custom_meta('property', 'og:%s' % name, value)


@register.simple_tag
def twitter_prop(name, value):
    return custom_meta('name', 'twitter:%s' % name, value)


@register.simple_tag
def facebook_prop(name, value):
    return '<meta name="fb:%s" content="%s">' % (name, value)


@register.simple_tag
def googleplus_prop(name, value):
    return custom_meta('itemprop', name, value)


@register.simple_tag
def googleplus_html_scope(value):
    """
    This is meant to be used as attribute to html / body or other tags to
    define schema.org type
    """
    return ' itemscope itemtype="http://schema.org/%s" ' % escape(value)


@register.simple_tag
def meta(name, value):
    return custom_meta('name', name, value)



@register.simple_tag
def custom_meta(key, name, value):
    return '<meta %s="%s" content="%s">' % (escape(key), escape(name), escape(value))



@register.simple_tag
def meta_list(name, lst):
    try:
        return custom_meta('name', name, ', '.join(lst))
    except:
        return ''


@register.simple_tag
def meta_extras(extra_props):
    return ' '.join([meta(name, extra_props[name]) if extra_props[name] else ''
                     for name in extra_props])


@register.simple_tag
def custom_meta_extras(extra_custom_props):
    return ' '.join([custom_meta(name_key, name_value, content) if content else ''
                     for name_key, name_value, content in extra_custom_props])


@register.simple_tag(takes_context=True)
def meta_namespaces(context):
    """
    Include OG namespaces. To be used in the <head> tag.
    """
    # do nothing if meta is not in context
    if not context.get('meta'):
        return ''

    meta = context['meta']
    namespaces = ['og: http://ogp.me/ns#']

    # add Facebook namespace
    if meta.use_facebook:
        namespaces.append('fb: http://ogp.me/ns/fb#')

    # add custom namespaces
    # needs to be after Facebook
    if meta.custom_namespace:
        custom_namespace = '%s: http://ogp.me/ns/%s#' % (
            meta.custom_namespace, meta.custom_namespace
        )
        namespaces.append(custom_namespace)

    return ' prefix="%s"' % " ".join(namespaces)
