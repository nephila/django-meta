===========
django-meta
===========

.. image:: https://img.shields.io/pypi/v/django-meta.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-meta
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/django-meta.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-meta
    :alt: Monthly downloads

.. image:: https://img.shields.io/pypi/pyversions/django-meta.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-meta
    :alt: Python versions

.. image:: https://img.shields.io/travis/nephila/django-meta.svg?style=flat-square
    :target: https://travis-ci.org/nephila/django-meta
    :alt: Latest Travis CI build status

.. image:: https://img.shields.io/coveralls/nephila/django-meta/master.svg?style=flat-square
    :target: https://coveralls.io/r/nephila/django-meta?branch=master
    :alt: Test coverage

.. image:: https://img.shields.io/codecov/c/github/nephila/django-meta/master.svg?style=flat-square
    :target: https://codecov.io/github/nephila/django-meta
    :alt: Test coverage

.. image:: https://codeclimate.com/github/nephila/django-meta/badges/gpa.svg?style=flat-square
   :target: https://codeclimate.com/github/nephila/django-meta
   :alt: Code Climate

This pluggable app allows Django developers to quickly add meta tags and
OpenGraph_, Twitter, and Google Plus properties to their HTML responses.


.. note:: django-meta is now maintained by Nephila on `github`_. Old bitbucket
          repository won't be updated anymore.

.. warning:: as of version 1.0 django-meta has included django-meta-mixin 0.2.1;
             django-meta 1.0 is a drop in replacement for django-meta-mixin:
             as a result django-meta-mixin is no longer actively developed

.. contents::

Installation
============

See https://django-meta.readthedocs.org/en/latest/installation.html

Supported versions
==================

Django
------

* Django 1.6
* Django 1.7
* Django 1.8
* Django 1.9


Python
------

* Python 2.6
* Python 2.7
* Python 3.3
* Python 3.4
* Python 3.5

Basic concept
=============

``django-meta`` provides a **view-method** and **model-method** interface to provide and handle meta informations

For more details check `documentation`_.

Authors and Contributors
========================

``django-meta`` has been started by `Branko Vukelic`_.

Current maintainer: `Iacopo Spalletti`_

See ``AUTHORS`` file for the complete list of contributors

Reporting bugs
==============

Please report all bugs to our Github `issue tracker`_.

.. _OpenGraph: http://opengraphprotocol.org/
.. _issue tracker: https://github.com/nephila/django-meta/issues/
.. _github: https://github.com/nephila/django-meta/
.. _Iacopo Spalletti: https://github.com/yakky
.. _documentation: http://django-meta.readthedocs.org/en/latest/
.. _Branko Vukelic: https://bitbucket.org/monwara

