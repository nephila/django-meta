Installation
============

* Install using pip::

    pip install django-meta


* Add ``meta`` and ``sekizai`` to ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ....
        'meta',
    )

* Add the :ref:`required namespace tags<rendering>` to your base template
  for compliancy with metadata protocols.
