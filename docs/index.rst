###########
django meta
###########

A pluggable app allows Django developers to quickly add meta tags and
OpenGraph_, Twitter, and Schema.org properties to their HTML responses.

.. warning:: **INCOMPATIBLE CHANGE**: as of version 2.0 django-meta has no
             longer supports Google+, basic Schema.org support has been introduced.

Usage
-----

django meta has two different operating mode:

 * :ref:`models`
 * :ref:`views`



.. toctree::
   :maxdepth: 2

   installation
   upgrading
   models
   views
   settings
   rendering
   extra_tags
   modules
   development
   contributing
   history

Apps using django-meta / extensions
-----------------------------------

* djangocms-blog: https://github.com/nephila/djangocms-blog
* djangocms-page-meta: https://github.com/nephila/djangocms-page-meta
* django-knocker: https://github.com/nephila/django-knocker
* wagtail-metadata-mixin: https://github.com/bashu/wagtail-metadata-mixin

Open a pull request to add yours here

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _OpenGraph: http://opengraphprotocol.org/
