.. _settings:

********
Settings
********


django-meta has a few configuration options that allow you to customize it. Two
of them are required: ``META_SITE_PROTOCOL`` and
``META_SITE_DOMAIN``.
By default, if they are unset, an ``ImproperlyConfigured`` exception will be
raised when dealing with ``url`` and ``image`` properties.
You can either set them, or overload the ``Meta`` class' ``get_domain`` and
``get_protocol`` methods (see :ref:`Meta object` section).

.. _META_SITE_PROTOCOL:

META_SITE_PROTOCOL
------------------

Defines the protocol used on your site. This should be set to either ``'http'``
or ``'https'``. Default is ``None``.

.. _META_SITE_DOMAIN:

META_SITE_DOMAIN
----------------

Domain of your site. The ``Meta`` objects can also be made to use the Django's
Sites framework as well (see :ref:`Meta object` and :ref:`META_USE_SITES` sections).
Default is ``None``.

.. _META_SITE_TYPE:

META_SITE_TYPE
--------------

The default ``og:type`` property to use site-wide. You do not need to set this
if you do not intend to use the OpenGraph properties. Default is ``None``.

.. _META_SITE_NAME:

META_SITE_NAME
--------------

The site name to use in ``og:site_name`` property. Althoug this can be
set per view, we recommend you set it globally. Defalt is ``None``.

.. _META_INCLUDE_KEYWORDS:

META_INCLUDE_KEYWORDS
---------------------

Iterable of extra keywords to include in every view. These keywords are
appended to whatever keywords you specify for the view, but are not used at all
if no keywords are specified for the view. See :ref:`META_DEFAULT_KEYWORDS` if you
wish to specify keywords to be used when no keywords are supplied. Default is
``[]``.

.. _META_DEFAULT_KEYWORDS:

META_DEFAULT_KEYWORDS
---------------------

Iterable of default keywords to use when no keywords are specified for the
view. These keywords are not included if you specify keywords for the view. If
you need keywords that will always be present, regardless of whether you've
specified any other keywords for the view or not, you need to combine this
setting with :ref:`META_INCLUDE_KEYWORDS` setting. Default is ``[]``.

.. _META_IMAGE_URL:

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

.. _META_USE_OG_PROPERTIES:

META_USE_OG_PROPERTIES
----------------------

This setting tells django-meta whether to render the OpenGraph properties.
Default is ``False``.

.. _META_USE_TWITTER_PROPERTIES:

META_USE_TWITTER_PROPERTIES
---------------------------

This setting tells django-meta whether to render the Twitter properties.
Default is ``False``.

.. _META_USE_GOOGLEPLUS_PROPERTIES:

META_USE_GOOGLEPLUS_PROPERTIES
------------------------------

This setting tells django-meta whether to render the Google properties.
Default is ``False``.

.. _META_USE_TITLE_TAG:

META_USE_TITLE_TAG
------------------

This setting tells django-meta whether to render the ``<title></title>`` tag.
Default is ``False``.

.. _META_USE_SITES:

META_USE_SITES
--------------

This setting tells django-meta to derive the site's domain using the Django's
sites contrib app. If you enable this setting, the :ref:`META_SITE_DOMAIN` is not
used at all. Default is ``False``.

META_OG_NAMESPACES
------------------

Use this setting to add a list of additional OpenGraph namespaces to be declared
in the ``<head>`` tag.


Other settings
--------------

The following settings are available to set a default value to the corresponding
attribute for both :ref:`views` and :ref:`models`

* image: ``META_DEFAULT_IMAGE`` (must be an absolute URL, ignores `META_IMAGE_URL`_)
* object_type: ``META_SITE_TYPE`` (default: first ``META_OBJECT_TYPES``)
* og_type: ``META_FB_TYPE`` (default: first ``META_FB_TYPES``)
* og_app_id: ``META_FB_APPID`` (default: blank)
* og_profile_id: ``META_FB_PROFILE_ID`` (default: blank)
* fb_pages: ``META_FB_PAGES`` (default: blank)
* og_publisher: ``META_FB_PUBLISHER`` (default: blank)
* og_author_url: ``META_FB_AUTHOR_URL`` (default: blank)
* twitter_type: ``META_TWITTER_TYPE`` (default: first ``META_TWITTER_TYPES``)
* twitter_site: ``META_TWITTER_SITE`` (default: blank)
* twitter_author: ``META_TWITTER_AUTHOR`` (default: blank)
* gplus_type: ``META_GPLUS_TYPE`` (default: first ``META_GPLUS_TYPES``)
* gplus_author: ``META_GPLUS_AUTHOR`` (default: blank)
* gplus_publisher: ``META_GPLUS_PUBLISHER`` (default: blank)
