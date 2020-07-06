Upgrading
============

When upgrading from version 1.x to 2.0 you must

* Replace ``META_GPLUS_TYPE`` with ``META_SCHEMAORG_TYPE``;
* Replace ``META_USE_GPLUS_PROPERTIES`` with ``META_USE_SCHEMAORG_PROPERTIES``;
* Remove all references to ``gplus_author``, ``gplus_publisher``;
* Replace all ``gplus_title``, ``gplus_description``, ``gplus_type``,
  ``use_gplus`` with the corresponding ``schemaorg`` attributes`;
* Replace all ``googleplus_prop``, ``googleplus_html_scope``, ``googleplus_scope``
  with the corresponding ``schemaorg`` templatetags;
