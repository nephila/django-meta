Installation
============

* Install using pip::

    pip install django-meta

* Add ``meta`` and ``sekizai`` to ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ....
        'meta',
        'sekizai',
    )

* Use one of the following:

    * Put ``sekizai.context_processors.sekizai`` into ``TEMPLATE_CONTEXT_PROCESSORS`` setting
      and use ``django.template.RequestContext`` when rendering your templates.

    * Use ``sekizai.context.SekizaiContext`` when rendering your templates.

What if I don't want to use sekizai?
------------------------------------

You can remove the sekizai dependency by removing
``{% addtoblock 'html_extra' %}{% googleplus_html_scope meta.gplus_type %}{% endaddtoblock %}``
from ``meta/templates/meta/meta.html`` template (do this by copying the template from ``meta``
to your own project like any other Django template) and change ``{% load sekizai_tags meta %}``
on top of the same file with ``{% load meta %}``
