.. _views:

************
View support
************

.. _Using the view:

Using the view
-----------------

You render the meta tags by including a ``meta.html`` partial template in your
view templates. This template will only render meta tags if it can find a
``meta`` object in the context, so you can safely include it in your base
template to have it render on all your pages.

The ``meta.html`` template expects to find an object called ``meta`` in
the template context which contains any of the following attributes:

+ use_og
+ use_twitter
+ use_facebook
+ use_schemaorg
+ use_title_tag
+ title
+ og_title
+ twitter_title
+ schemaorg_title
+ description
+ keywords
+ url
+ image
+ image_object
+ image_width
+ image_height
+ object_type
+ site_name
+ twitter_site
+ twitter_creator
+ twitter_type
+ facebook_app_id
+ locale
+ extra_props
+ extra_custom_props

In all cases, if the attribute is not set/empty, the matching metadata/property is not
rendered.

.. note:: attribute ``twitter_card`` is available as deprecated attribute with the
          same meaning of ``twitter_type``. It will be removed in version 3.0,
          so update your code accordingly.


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
        },
        extra_custom_props=[
            ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
        ]
    )

When the time comes to render the template, you **must** include the instance as
``'meta'`` context variable. In case you use class-based views check the `view mixin`_
helper, for function based views you must pass the ``meta`` object manually to the context
where needed.

``Meta`` also accept an (optional) ``request`` argument to pass the current
request, which is used to retrieve the ``SITE_ID`` if it's not in the settings.

The ``Meta`` instances have the same properties as the keys listed in the
`Using the view`_ section. For convenience, some of the properties are 'smart',
and will modify values you set. These properties are:

+ keywords
+ url
+ image
+ image_object

For brevity, we will only discuss those here.

Meta.keywords
~~~~~~~~~~~~~

When you assign keywords either via the constructor, or by assigning an
iterable to the ``keywords`` property, it will be cleaned up of all duplicates
and returned as a ``set``. If you have specified the :ref:`META_INCLUDE_KEYWORDS`,
the resulting set will also include them. If you omit this argument when
instantiating the object, or if you assign ``None`` to the ``keywords``
property, keywords defined by :ref:`META_DEFAULT_KEYWORDS` setting will be used
instead.

Meta.url
~~~~~~~~~~~~~

Setting the url behaves differently depending on whether you are passing a
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

Meta.image_object
~~~~~~~~~~~~~~~~~

The ``image_object`` property is the most complete way to provide image meta.

To use this property, you must pass a dictionary with at least the ``url`` attribute.

All others keys will be rendered alongside the ``url``, if the specific protocol
provides it.

Currently only OpenGraph support more than the image url, and you might add:

* ``width``: image width
* ``height``: image height
* ``alt``: alternate image description
* ``secure_url``: https URL for the image, if different than the ``url`` key
* ``type``: image mime type

example::

    media = {
        'url': 'http://meta.example.com/image.gif',
        'secure_url': 'https://meta.example.com/custom.gif',
        'type': 'some/mime',
        'width': 100,
        'height': 100,
        'alt': 'a media',
    }

it will be rendered as::

    <meta property="og:image:alt" content="a media">
    <meta property="og:image:height" content="100">
    <meta property="og:image:secure_url" content="https://meta.example.com/image.gif">
    <meta property="og:image:type" content="some/mime">
    <meta property="og:image:url" content="http://meta.example.com/image.gif">
    <meta property="og:image:width" content="100">

.. note: as of version 2.0, this is the preferred way to set image information.


Meta.image
~~~~~~~~~~~~~

The ``image`` property behaves the same way as ``url`` property with one
notable difference. This property treats absolute and relative paths
differently. It will place relative paths under the :ref:`META_IMAGE_URL`.

if ``image_object`` is provided, it takes precedence over this property, for all
the protocols, even if they only support the image URL.

.. _view mixin:

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
receive a ``context`` keyword argument containing the request context.

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
~~~~~~~~~~~~~

This key contains a boolean value, and instructs the template to render the
OpenGraph_ properties. These are usually used by FaceBook to get more
information about your site's pages.

use_twitter
~~~~~~~~~~~~~

This key contains a boolean value, and instructs the template to render the
Twitter properties. These are usually used by Twitter to get more
information about your site's pages.

use_facebook
~~~~~~~~~~~~~

This key contains a boolean value, and instructs the template to render the
Facebook properties. These are usually used by Facebook to get more
information about your site's pages.

use_schemaorg
~~~~~~~~~~~~~~~~~~~

This key contains a boolean value, and instructs the template to render the
Google+. These are usually used by Google to get more information about your
site's pages.

use_title_tag
~~~~~~~~~~~~~

This key contains a boolean value, and instructs the template to render the
``<title></title>`` tag. In the simple case, you use ``<title></title>`` tag
in the templates where you can override it, but if you want to generate it
dynamically in the views, you can set this property to ``True``.

title
~~~~~~~~~~~~~

This key is used in the ``og:title`` OpenGraph property if ``use_og`` is
``True``, ``twitter:title`` if ``use_twitter`` is ``True``,
``itemprop="title"`` if ``use_schemaorg`` is ``True`` or ``<title></title>`` tag
if ``use_title_tag`` is ``True``.

The service-specific variants are also supported:

* ``og_title``
* ``twitter_title``
* ``schema_title``

If set on the ``Meta`` object, they will be used instead of the generic title
which will be used as a fallback.

description
~~~~~~~~~~~~~

This key is used to render the ``description`` meta tag as well as the
``og:description`` and ``twitter:description`` property.

keywords
~~~~~~~~~~~~~

This key should be an iterable containing the keywords for the page. It is used
to render the ``keywords`` meta tag.

url
~~~~~~~~~~~~~

This key should be the *full* URL of the page. It is used to render the
``og:url``, ``twitter:url``, ``itemprop=url`` property.

image_object
~~~~~~~~~~~~~

This key must be set to a dictionary containing at least the ``url`` key, additional
keys will be rendered if supported by each protocol. Currently only OpenGraph supports
additional image properties.

Example::

    media = {
        'url': 'http://meta.example.com/image.gif',
        'secure_url': 'https://meta.example.com/custom.gif',
        'type': 'some/mime',
        'width': 100,
        'height': 100,
        'alt': 'a media',
    }

image
~~~~~~~~~~~~~

This key should be the *full* URL of an image to be used with the ``og:image``,
``twitter:image``, ``itemprop=image`` property.

image_width
~~~~~~~~~~~~~

This key should be the width of image. It is used to render ``og:image:width`` value

image_height
~~~~~~~~~~~~~

This key should be the height of image. It is used to render ``og:image:height`` value

object_type
~~~~~~~~~~~~~

This key is used to render the ``og:type`` property.

site_name
~~~~~~~~~~~~~

This key is used to render the ``og:site_name`` property.

twitter_site
~~~~~~~~~~~~~

This key is used to render the ``twitter:site`` property.

twitter_creator
~~~~~~~~~~~~~~~~~~~

This key is used to render the ``twitter:creator`` property.

twitter_type
~~~~~~~~~~~~~

This key is used to render the ``twitter:card`` property.

facebook_app_id
~~~~~~~~~~~~~~~~~~~

This key is used to render the ``fb:app_id`` property.

locale
~~~~~~~~~~~~~

This key is used to render the ``og:locale`` property.

extra_props
~~~~~~~~~~~~~

A dictionary of extra optional properties::

    {
        'foo': 'bar',
        'key': 'value'
    }

    ...

    <meta name="foo" content="bar">
    <meta name="key" content="value">

See :ref:`Adding custom tags / properties <extra_tags_views>` for details.

extra_custom_props
~~~~~~~~~~~~~~~~~~~

A list of tuples for rendering custom extra properties::

    [
        ('key', 'foo', 'bar')
        ('property', 'name', 'value')
    ]

    ...

    <meta name="foo" content="bar">
    <meta property="name" content="value">

.. _OpenGraph: http://opengraphprotocol.org/
