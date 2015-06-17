===========
django-meta
===========

.. image:: https://pypip.in/version/django-meta/badge.png
    :target: https://pypi.python.org/pypi/django-meta/
    :alt: Latest Version

.. image:: https://travis-ci.org/nephila/django-meta.svg?branch=develop
    :target: https://travis-ci.org/nephila/django-meta
    :alt: Travis status

.. image:: https://coveralls.io/repos/nephila/django-meta/badge.png?branch=develop
    :target: https://coveralls.io/r/nephila/django-meta
    :alt: Coveralls status

.. image:: https://pypip.in/download/django-meta/badge.png
    :target: https://pypi.python.org/pypi//django-meta/
    :alt: Download

.. image:: https://pypip.in/wheel/django-meta/badge.png
    :target: https://pypi.python.org/pypi/django-meta/
    :alt: Wheel Status

.. image:: https://pypip.in/license/django-meta/badge.png
    :target: https://pypi.python.org/pypi/django-meta/
    :alt: License

This pluggable app allows Django developers to quickly add meta tags and
OpenGraph_, Twitter, and Google Plus properties to their HTML responses.


.. note:: django-meta is now maintained by Nephila on `github`_. Old bitbucket
          repository won't be updated anymore.

.. contents::

Installation
============

Install using pip::

    pip install django-meta

Add ``meta`` to ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ....
        'meta',
    )

Basic concept
=============

You render the meta tags by including a ``meta.html`` parial template in your
view templates. This template will only render meta tags if it can find a
``meta`` object in the context, so you can safely include it in your base
template to have it render on all your pages.

The ``meta.html`` template expects to find a dict or object called ``meta`` in
the template context. In that dict or object, it will expect to find any of the
following keys/attributes:

+ use_og
+ use_twitter
+ use_facebook
+ use_googleplus
+ title
+ description
+ keywords
+ url
+ image
+ object_type
+ site_name
+ twitter_site
+ facebook_app_id
+ locale
+ extra_props
+ extra_custom_props

In all cases, if the key is omitted, the matching metadata/property is not 
rendered.

use_og
------

This key contains a boolean value, and instructs the template to render the
OpenGraph_ properties. These are usually used by FaceBook to get more
information about your site's pages.

use_twitter
-----------

This key contains a boolean value, and instructs the template to render the
Twitter properties. These are usually used by Twitter to get more
information about your site's pages.

use_facebook
-----------

This key contains a boolean value, and instructs the template to render the
Facebook properties. These are usually used by Facebook to get more
information about your site's pages.

use_googleplus
--------------

This key contains a boolean value, and instructs the template to render the
Google+. These are usually used by Google to get more information about your
site's pages.

title
-----

This key is used in the ``og:title`` OpenGraph property, if ``use_og`` is
``True``, ``twitter:title`` if ``use_twitter`` is ``True`` or
``itemprop="title"`` if ``use_googleplus`` is ``True``.

description
-----------

This key is used to render the ``description`` meta tag as well as the
``og:description`` and ``twitter:description`` property.

keywords
--------

This key should be an iterable containing the keywords for the page. It is used
to render the ``keywords`` meta tag.

url
---

This key should be the *full* URL of the page. It is used to render the
``og:url``, ``twitter:url``, ``itemprop=url`` property.

image
-----

This key should be the *full* URL of an image to be used with the ``og:image``,
``twitter:image``, ``itemprop=mage`` property.

object_type
-----------

This key is used to render the ``og:type`` property.

site_name
---------

This key is used to render the ``og:site_name`` property.

twitter_site
------------

This key is used to render the ``twitter:site`` property.

facebook_app_id
------------

This key is used to render the ``fb:app_id`` property.

locale
------

This key is used to render the ``og:locale`` property.

extra_props
-----------

A dictionary of extra optional properties.

    {
        'foo': 'bar',
        'key': 'value'
    }

    ...

    <meta name="foo" content="bar">
    <meta name="key" content="value">

extra_custom_props
------------------

A list of tuples for rendering custom extra properties.

    [
        ('key', 'foo', 'bar')
        ('property', 'name', 'value')
    ]

    ...

    <meta name="foo" content="bar">
    <meta property="name" content="value">

Meta objects
============

The core of django-meta is the ``Meta`` class. Although you can prepare the
metadata for the template yourself, this class can make things somewhat
easier.

To set up a meta object for use in templates, simply instantiate it with the
properties you want to use::

    from meta.views import Meta

    meta = Meta(
        title="Sam's awesome ponies",
        description='Awesome page about ponies',
        keywords=['pony', 'ponies', 'awesome'],
        extra_props = {
            'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
        }
        'extra_custom_props': [
            ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
        ]
    )

When the time comes to render the template, simply include the instance as
``'meta'`` context variable.

The ``Meta`` instances have the same properties as the keys listed in the
`Basic concept`_ section. For convenience, some of the properties are 'smart',
and will modify values you set. These properties are:

+ keywords
+ url
+ image

For brevity, we will only discuss those here.

Meta.keywords
-------------

When you assign keywords either via the constructor, or by assigning an
iterable to the ``keywords`` property, it will be cleaned up of all duplicates
and returned as a ``set``. If you have specified the META_INCLUDE_KEYWORDS_,
the resulting set will also include them. If you omit this argument when
instantiating the object, or if you assign ``None`` to the ``keywords``
property, keywords defined by META_DEFAULT_KEYWORDS_ setting will be used
instead.

Meta.url
--------

Setting the url behaves differently depending on whether you are passsing a
path or a full URL. If your URL starts with ``'http'``, it will be used
verbatim (not that the actual validity of the url is not checked so
``'httpfoo'`` will be considered a valid URL). If you use an absolute or
relative path, domain and protocol parts would be prepended to the URL. Here's
an example::

    m = Meta(url='/foo/bar')
    m.url  # returns 'http://example.com/foo/bar'

The actual protocol and domain are dependent on the META_SITE_PROTOCOL_ and
META_SITE_DOMAIN_ settings. If you wish to use the Django's sites contrib app
to calculate the domain, you can either set the META_USE_SITES_ setting to
``True``, or pass the ``use_sites`` argument to the constructor::

    m = Meta(url='/foo/bar', use_sites=True)

Note that using the sites app will trigger database queries and/or cache hits,
and it is therefore disabled by default.

Meta.image
----------

The ``image`` property behaves the same way as ``url`` property with one
notable difference. This property treats absolute and relative paths
differently. It will place relative paths under the META_IMAGE_URL_.

View mixin
==========

As a convenience to those who embrace the Django's class-based views,
django-meta includes a mixin that can be used with your views. Using the mixin
is very simple::

    from django.views.generic import View

    from meta.views import MetadataMixin


    class MyView(MetadataMixin, View):
        title = 'Some page'
        description = 'This is an awesome page'
        image = 'img/some_page_thumb.gif'
        url = 'some/page/'
        
        ....


The mixin sports all properties listed in the `Basic concept`_ section with a
few additional bells and whistles that make working with them easier. The mixin
will return an instance of the ``Meta`` class (see `Meta objects`_) as ``meta`` 
context variable. This is, in turn, used in the partial template to render the
meta tags (see `Rendering meta tags`_).

Each of the properties on the mixin can be calculated dynamically by using the
``MetadataMixin.get_meta_PROPERTYNAME`` methods, where ``PROPERTYNAME`` is the
name of the property you wish the calculate at runtime. Each method will
receive a ``context`` keyword argument containig the request context.

For example, to calculate the description dynamically, you may use the mixin
like so::

    class MyView(MetadataMixin, SingleObjectMixin, View):
        ...

        def get_meta_description(self, context):
            return self.get_object().description

There are two more methods that you can overload in your view classes, and
those are ``get_domain`` and ``get_protocol``.

Rendering meta tags
===================

To render the meta tags, simply add the ``meta`` dictionary/object to the
template context, and add this inside the ``<head>`` tags::

    {% include 'meta.html' %}

The partial template will not output anything if the context dictionary does
not contain a ``meta`` object, so you can safely include it in your base
template.

Additionally, if you want to use facebook or a custom namespace, you should include
them in the <head> tag, as follow:

    {% load meta %}
    <head {% meta_namespaces %} >

This will take care of rendering OpenGraph namespaces in the ``<head prefix="...">``.

Configuration
=============

django-meta has a few configuration options that allow you to customize it. Two
of them are required. Those are ``META_SITE_PROTOCOL`` and
``META_SITE_DOMAIN``. By default, if they are unset, an
``ImproperlyConfigured`` exception will raised when dealing with ``url`` and
``image`` properties. You can either set them, or overload the ``Meta`` class'
``get_domain`` and ``get_protocol`` methods (see `Meta objects`_ section).

META_SITE_PROTOCOL
------------------

Defines the protocol used on your site. This should be set to either ``'http'``
or ``'https'``. Default is ``None``.

META_SITE_DOMAIN
----------------

Domain of your site. The ``Meta`` objects can also be made to use the Django's
Sites framework as well (see `Meta objects`_ and META_USE_SITES_ sections).
Default is ``None``.

META_SITE_TYPE
--------------

The default ``og:type`` property to use site-wide. You do not need to set this
if you do not intend to use the OpenGraph properties. Default is ``None``.

META_SITE_NAME
--------------

The site name to use in ``og:site_name`` property. Althoug this can be
set per view, we recommend you set it globally. Defalt is ``None``.

META_INCLUDE_KEYWORDS
---------------------

Iterable of extra keywords to include in every view. These keywords are
appended to whatever keywords you specify for the view, but are not used at all
if no keywords are specified for the view. See META_DEFAULT_KEYWORDS_ if you
wish to specify keywords to be used when no keywords are supplied. Default is
``[]``.

META_DEFAULT_KEYWORDS
---------------------

Iterable of default keywords to use when no keywords are specified for the
view. These keywords are not included if you specify keywords for the view. If
you need keywords that will always be present, regardless of whether you've
specified any other keywords for the view or not, you need to combine this
setting with META_INCLUDE_KEYWORDS_ setting. Default is ``[]``.

META_IMAGE_URL
--------------

This setting is used as the base URL for all image assets that you intend to
use as ``og:image`` property in your views. This is django-meta's counterpart
of the Django's ``STATIC_URL`` setting. In fact, Django's ``STATIC_URL``
setting is a fallback if you do not specify this setting, so make sure either
one is configured. Default is to use the ``STATIC_URL`` setting. 

Note that you must add the trailing slash when specifying the URL. Even if you
do not intend to use the ``og:image`` property, you need to define either this
setting or the ``STATIC_URL`` setting or an attribute error will be raised.

META_USE_OG_PROPERTIES
----------------------

This setting tells django-meta whether to render the OpenGraph properties.
Default is ``False``.

META_USE_TWITTER_PROPERTIES
---------------------------

This setting tells django-meta whether to render the Twitter properties.
Default is ``False``.

META_USE_GOOGLEPLUS_PROPERTIES
------------------------------

This setting tells django-meta whether to render the Google properties.
Default is ``False``.

META_USE_SITES
--------------

This setting tells django-meta to derive the site's domain using the Django's
sites contrib app. If you enable this setting, the META_SITE_DOMAIN_ is not 
used at all. Default is ``False``. 

Authors and Contributors
========================

``django-meta`` has been started by `Branko Vukelic`_.

Current maintainer: `Iacopo Spalletti`_

We thank the contributors to this project:

+ leifdenby_

Reporting bugs
==============

Please report all bugs to our Github `issue tracker`_.

.. _OpenGraph: http://opengraphprotocol.org/
.. _issue tracker: https://github.com/nephila/django-meta/issues/
.. _github: https://github.com/nephila/django-meta/
.. _leifdenby: https://bitbucket.org/leifdenby
.. _Iacopo Spalletti: https://github.com/yakky
.. _Branko Vukelic: https://bitbucket.org/monwara

