.. _views:

************
View support
************

.. _Using the view:

Using the view
--------------

You render the meta tags by including a ``meta.html`` partial template in your
view templates. This template will only render meta tags if it can find a
``meta`` object in the context, so you can safely include it in your base
template to have it render on all your pages.

The ``meta.html`` template expects to find an object called ``meta`` in
the template context which contains any of the following attributes:

+ use_og
+ use_twitter
+ use_facebook
+ use_googleplus
+ use_title_tag
+ title
+ description
+ keywords
+ url
+ image
+ object_type
+ site_name
+ twitter_site
+ twitter_creator
+ twitter_card
+ facebook_app_id
+ locale
+ extra_props
+ extra_custom_props

In all cases, if the attribute is not set/empty, the matching metadata/property is not
rendered.

.. _meta object:

Meta object
===========

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
`Using the view`_ section. For convenience, some of the properties are 'smart',
and will modify values you set. These properties are:

+ keywords
+ url
+ image

For brevity, we will only discuss those here.

Meta.keywords
-------------

When you assign keywords either via the constructor, or by assigning an
iterable to the ``keywords`` property, it will be cleaned up of all duplicates
and returned as a ``set``. If you have specified the :ref:`META_INCLUDE_KEYWORDS`,
the resulting set will also include them. If you omit this argument when
instantiating the object, or if you assign ``None`` to the ``keywords``
property, keywords defined by :ref:`META_DEFAULT_KEYWORDS` setting will be used
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

The actual protocol and domain are dependent on the :ref:`META_SITE_PROTOCOL` and
:ref:`META_SITE_DOMAIN` settings. If you wish to use the Django's sites contrib app
to calculate the domain, you can either set the :ref:`META_USE_SITES` setting to
``True``, or pass the ``use_sites`` argument to the constructor::

    m = Meta(url='/foo/bar', use_sites=True)

Note that using the sites app will trigger database queries and/or cache hits,
and it is therefore disabled by default.

Meta.image
----------

The ``image`` property behaves the same way as ``url`` property with one
notable difference. This property treats absolute and relative paths
differently. It will place relative paths under the :ref:`META_IMAGE_URL`.

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


The mixin sports all properties listed in the :ref:`Using the view` section with a
few additional bells and whistles that make working with them easier. The mixin
will return an instance of the ``Meta`` class (see :ref:`Meta object`) as ``meta``
context variable. This is, in turn, used in the partial template to render the
meta tags (see :ref:`rendering`).

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

Reference template
==================

See below the basic reference template::

    {% load sekizai_tags meta %}

    <html {% render_block 'html_extra' %}>
    <head {% meta_namespaces %}>
        {{ meta.og_description }}
        {% include "meta/meta.html" %}
    </head>
    <body>
    {% block content %}
    {% endblock content %}
    </body>
    </html>


Properties
==========

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
------------

This key contains a boolean value, and instructs the template to render the
Facebook properties. These are usually used by Facebook to get more
information about your site's pages.

use_googleplus
--------------

This key contains a boolean value, and instructs the template to render the
Google+. These are usually used by Google to get more information about your
site's pages.

use_title_tag
-------------

This key contains a boolean value, and instructs the template to render the
``<title></title>`` tag. In the simple case, you use ``<title></title>`` tag
in the templates where you can override it, but if you want to generate it
dynamically in the views, you can set this property to ``True``.

title
-----

This key is used in the ``og:title`` OpenGraph property if ``use_og`` is
``True``, ``twitter:title`` if ``use_twitter`` is ``True``,
``itemprop="title"`` if ``use_googleplus`` is ``True`` or ``<title></title>`` tag
if ``use_title_tag`` is ``True``.

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

twitter_creator
---------------

This key is used to render the ``twitter:creator`` property.

twitter_card
------------

This key is used to render the ``twitter:card`` property.

facebook_app_id
---------------

This key is used to render the ``fb:app_id`` property.

locale
------

This key is used to render the ``og:locale`` property.

extra_props
-----------

A dictionary of extra optional properties::

    {
        'foo': 'bar',
        'key': 'value'
    }

    ...

    <meta name="foo" content="bar">
    <meta name="key" content="value">

extra_custom_props
------------------

A list of tuples for rendering custom extra properties::

    [
        ('key', 'foo', 'bar')
        ('property', 'name', 'value')
    ]

    ...

    <meta name="foo" content="bar">
    <meta property="name" content="value">

.. _OpenGraph: http://opengraphprotocol.org/
