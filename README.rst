===========
django-meta
===========

|Gitter| |PyPiVersion| |PyVersion| |GAStatus| |TestCoverage| |CodeClimate| |License|

This pluggable app allows Django developers to quickly add meta tags and
OpenGraph_, Twitter, and Schema.org properties to their HTML responses.

.. warning:: **INCOMPATIBLE CHANGE**: as of version 2.0 django-meta has no
             longer supports Google+, basic Schema.org support has been introduced.

.. contents::

************
Installation
************

See https://django-meta.readthedocs.io/en/latest/installation.html

******************
Supported versions
******************

******
Django
******

2.2 to 4.0 (newer versions might work but are not tested yet)


******
Python
******

Python 3.7 to 3.10

*************
Basic concept
*************

``django-meta`` provides a **view-method** and **model-method** interface to provide and handle meta informations

For more details check `documentation`_.

**************************
Authors and Contributors
**************************

``django-meta`` has been started by `Branko Vukelic`_.

Current maintainer: `Iacopo Spalletti`_

See ``AUTHORS`` file for the complete list of contributors

***********************************
Apps using django-meta / extensions
***********************************

See `third_party_apps`_

**************
Reporting bugs
**************

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

.. |GAStatus| image:: https://github.com/nephila/django-meta/workflows/Tox%20tests/badge.svg
    :target: https://github.com/nephila/django-meta
    :alt: Latest CI build status

.. |TestCoverage| image:: https://img.shields.io/coveralls/nephila/django-meta/master.svg?style=flat-square
    :target: https://coveralls.io/r/nephila/django-meta?branch=master
    :alt: Test coverage

.. |License| image:: https://img.shields.io/github/license/nephila/django-meta.svg?style=flat-square
   :target: https://pypi.python.org/pypi/django-meta/
    :alt: License

.. |CodeClimate| image:: https://codeclimate.com/github/nephila/django-meta/badges/gpa.svg?style=flat-square
   :target: https://codeclimate.com/github/nephila/django-meta
   :alt: Code Climate
