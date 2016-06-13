Installation
============

* Install using pip::

    pip install django-meta


* Add ``meta`` to ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ....
        'meta',
    )

* Add the :ref:`required namespace tags<rendering>` to your base template
  for compliancy with metadata protocols.

* Optionally you can install and configure `sekizai`_


.. _sekizai: https://django-sekizai.readthedocs.io/en/latest/#usage
