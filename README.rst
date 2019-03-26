===========
django-meta
===========

|Gitter| |PyPiVersion| |PyVersion| |Status| |TestCoverage| |CodeClimate| |License|

This pluggable app allows Django developers to quickly add meta tags and
OpenGraph_ and Twitter properties to their HTML responses.


.. note:: django-meta is now maintained by Nephila on `github`_. Old bitbucket
          repository won't be updated anymore.

.. warning:: as of version 1.0 django-meta has included django-meta-mixin 0.2.1;
             django-meta 1.0 is a drop in replacement for django-meta-mixin:
             as a result django-meta-mixin is no longer actively developed

.. warning:: As of version 1.4, the support for Python 2.6 and Django<1.8 has been dropped

.. contents::

Installation
============

See https://django-meta.readthedocs.io/en/latest/installation.html

Supported versions
==================

Django
------

1.11 to 2.2 (newer versions might work but are not tested yet)


Python
------

Python 2.7, 3.5, 3.6, 3.7

Basic concept
=============

``django-meta`` provides a **view-method** and **model-method** interface to provide and handle meta informations

For more details check `documentation`_.

Authors and Contributors
========================

``django-meta`` has been started by `Branko Vukelic`_.

Current maintainer: `Iacopo Spalletti`_

See ``AUTHORS`` file for the complete list of contributors

Apps using django-meta / extensions
===================================

See `third_party_apps`_

Reporting bugs
==============

Please report all bugs to our Github `issue tracker`_.

.. _OpenGraph: http://opengraphprotocol.org/
.. _issue tracker: https://github.com/nephila/django-meta/issues/
.. _github: https://github.com/nephila/django-meta/
.. _Iacopo Spalletti: https://github.com/yakky
.. _documentation: https://django-meta.readthedocs.io/en/latest/
.. _third_party_apps: https://django-meta.readthedocs.io/en/latest/#apps-using-django-meta-extensions
.. _Branko Vukelic: https://bitbucket.org/monwara




.. |Gitter| image:: https://img.shields.io/badge/GITTER-join%20chat-brightgreen.svg?style=flat-square
    :target: https://gitter.im/nephila/applications
    :alt: Join the Gitter chat

.. |PyPiVersion| image:: https://img.shields.io/pypi/v/django-meta.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-meta
    :alt: Latest PyPI version

.. |PyVersion| image:: https://img.shields.io/pypi/pyversions/django-meta.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-meta
    :alt: Python versions

.. |Status| image:: https://img.shields.io/travis/nephila/django-meta.svg?style=flat-square
    :target: https://travis-ci.org/nephila/django-meta
    :alt: Latest Travis CI build status

.. |TestCoverage| image:: https://img.shields.io/coveralls/nephila/django-meta/master.svg?style=flat-square
    :target: https://coveralls.io/r/nephila/django-meta?branch=master
    :alt: Test coverage

.. |License| image:: https://img.shields.io/github/license/nephila/django-meta.svg?style=flat-square
   :target: https://pypi.python.org/pypi/django-meta/
    :alt: License

.. |CodeClimate| image:: https://codeclimate.com/github/nephila/django-meta/badges/gpa.svg?style=flat-square
   :target: https://codeclimate.com/github/nephila/django-meta
   :alt: Code Climate
