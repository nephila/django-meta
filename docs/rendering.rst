.. _rendering:

*******************
Rendering meta tags
*******************

To render the meta tags, simply add the ``meta`` dictionary/object to the
template context, and add this inside the ``<head>`` tags::

    {% include 'meta/meta.html' %}

The partial template will not output anything if the context dictionary does
not contain a ``meta`` object, so you can safely include it in your base
template.

Additionally, if you want to use facebook or a custom namespace, you should include
them in the <head> tag, as follow::

    {% load meta %}
    ...
    <head {% meta_namespaces %} >

This will take care of rendering OpenGraph namespaces in the ``<head prefix="...">``.

If you enabled Google+ Support you have to add the following templatetag to the ``<html>`` tag::

    {% load meta %}
    ...
    <html {% meta_namespaces_gplus %}>

For compatibility with 1.0 and previous version you can keep the sekizai version of the above::

    {% load sekizai_tags meta %}
    ...
    <html {% render_block 'html_extra' %}>
