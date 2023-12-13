.. :changelog:

*******
History
*******

.. towncrier release notes start

2.4.1 (2023-12-13)
==================

Features
--------

- Remove useless "else" statements. (#182)
- Switch to Coveralls Github action (#188)


Bugfixes
--------

- Refactor FullUrlMixin get_domain to handle django.contrib.sites not in INSTALLED_APPS (#192)


2.4.0 (2023-09-25)
==================

Features
--------

- Add schema.org support (#76)
- Refactor settings to make override_settings in tests more consistent (#167)
- Migrate to bump-my-version (#173)


2.3.0 (2023-08-10)
==================

Bugfixes
--------

- Fix schemaorg_description not being in Meta class (#127)
- Fix schema.org protocol to be https (#152)
- Fix request set order in Meta.__init__ (#155)


2.2.0 (2023-04-18)
==================

Features
--------

- Move to ruff (#138)
- Add support for Django 4.2 (#144)


2.1.0 (2022-07-28)
==================

Bugfixes
--------

- Changes imports from ugettext_lazy to gettext_lazy to fix deprecation warning (#130)
- Get correct setting META_USE_SITES in build_absolute_uri model method (#133)
- Update tox environments and github actions (#135)


2.0.0 (2020-11-14)
==================

Features
--------

- Drop Python 2 (#118)
- Drop Django<2.2 (#118)
- Add Django 3.1 (#118)
- Update tooling (#118)
- Port to github-actions (#118)
- Remove G+ support - Replace with Schema.org (#108)
- Add support for image object (#114)


Bugfixes
--------

- Switch request handling to thread locals (#115)


1.7.0 (2020-07-07)
==================

* Fixed support for secure_url
* Normalized twitter_card / twitter_type attributes

1.6.1 (2020-01-16)
==================

* Added explicit dependency on six
* Added python 3.8

1.6.0 (2019-12-22)
==================

* Added Django 3.0 support
* Moved to django-app-helper
* Improved documentation regarding extra / custom props

1.5.2 (2019-07-02)
==================

* Added image size for facebook sharing

1.5.1 (2019-04-11)
==================

* Fixed error if the property referenced in _metadata returns False


1.5.0 (2019-03-23)
==================

* Added support for Django 2.1 and 2.2
* Added support for Python 3.7
* Dropped support for Django < 1.11
* Dropped  support for Python 3.4
* Fixed support for og:image:secure_url
* Fixed minor documentation error
* Added support for service-specific titles

1.4.1 (2018-01-21)
==================

* Added Django 2.0 support
* Fixed RTD builds
* Fixed MetadataMixin.use_use_title_tag typo
* Add request to Meta arguments

1.4.0 (2017-08-12)
==================

* Add Django 1.11 support
* Drop python 2.6/ Django<1.8
* Wrap meta.html content in spaceless templatetag to suppress redundant newlines
* Fix issue in Django 1.10

1.3.2 (2016-10-26)
==================

* Fix error if custom_meta_extras is empty
* Fix twitter properties
* Fix error with META_DEFAULT_IMAGE path

1.3.1 (2016-08-01)
==================

* Add support for G+ publisher tag

1.3 (2016-06-06)
================

* Added support for fb_pages attribute
* Properly implement META_DEFAULT_IMAGE for view-based mixins
* Fixed error in facebook_prop templatetag
* Removed dependency of sites framework

1.2 (2016-04-09)
================

* Fix issue when emulating sekizai

1.1 (2016-04-08)
================

* Sekizai is not required anymore

1.0 (2016-03-29)
================

* Merge with django-meta-mixin
* Reorganized documentation
* Remove deprecated ``make_full_url`` method
* Add _retrieve_data interface for generic attribute data generation

0.3.2 (2016-02-09)
==================

* Use autoescape off in template for Django 1.9

0.3.1 (2015-06-27)
==================

* Bump for re-upload

0.3.0 (2015-06-27)
==================

* Add support for more twitter attributes
* Add support for more facebook attributes
* Official support for Django 1.4->1.8
* Official support for Python 2.6, 2.7, 3.2, 3.3, 3.4

0.2.1 (2014-12-15)
==================

* Add support for more attributes
* Add templatetag to handle generic attributes

0.2.0 (2014-05-28)
==================

* Code cleanup
* Change maintainership information
* Official Python 3 support

0.1.0 (2014-01-20)
==================

* Support for Twitter meta data (leifdenby)
* Fixes to OpenGraph tags (leifdenby)
* Support Google Plus tags (Iacopo Spalletti)

0.0.3 (2013-11-12)
==================

* Keywords are now order-preserving
* Keywords are no longer a set(), but a normal list

0.0.2 (2013-04-12)
==================

* Fixed keywords not being included in metadata
* Fixed get_meta_class not being used in the mixin

0.0.1 (2013-04-04)
==================

* Initial version
