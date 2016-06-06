.. :changelog:

*******
History
*******

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
