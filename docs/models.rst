.. _models:

*************
Model support
*************

Concepts
--------

**django-meta** provides a mixin to handle metadata in your models.

Actual data are evaluated at runtime pulling values from model attributes and
methods.

To use it, defines a ``_metadata`` attribute as a dictionary of tag/value pairs;

* **tag** is the name of the metatag as used by ``meta.html`` template
* **value** is a string that is evaluated in the following order:

  * model method name called with the meta attribute as argument
  * model method name called with no arguments
  * model attribute name (evaluated at runtime)
  * string literal (if none of the above exists)

If **value** is ``False`` or it is evaluated as ``False`` at runtime the tag is skipped.

To use this mixin you must invoke ``as_meta()`` on the model instance
for example in the get_context_data().

You can also add custom tags / properties. See :ref:`Adding custom tags / properties <extra_tags_views>` for details.

Request
+++++++

``as_meta()`` accepts the ``request`` object that is saved locally and is available to methods by
using the ``get_request`` method.


Public interface
++++++++++++++++

``ModelMeta.get_meta(request=None)``: returns the metadata attributes definition. Tipically these
are set in ``_metadata`` attribute in the model;

``ModelMeta.as_meta(request=None)``: returns the meta representation of the object suitable for
use in the template;

``ModelMeta.get_request()``: returns the ``request`` object, if given as argument to ``as_meta``;

``ModelMeta.get_author()``: returns the author object for the current instance. Default
implementation does not return a valid object, this **must** be overridden in the application
according to what is an author in the application domain;

``ModelMeta.build_absolute_uri(url)``: create an absolute URL (i.e.: complete with protocol and
domain); this is generated from the ``request`` object, if given as argument to ``as_meta``;


.. _model_metadata:

Usage
-----

#. Configure ``django-meta`` according to documentation

#. Add meta information to your model::

    from django.db import models
    from meta.models import ModelMeta

    class MyModel(ModelMeta, models.Model):
        name = models.CharField(max_length=20)
        abstract = models.TextField()
        image = models.ImageField()
        ...

        _metadata = {
            'title': 'name',
            'description': 'abstract',
            'image': 'get_meta_image',
            ...
        }
        def get_meta_image(self):
            if self.image:
                return self.image.url

#. Push metadata in the context using ``as_meta`` method::

    class MyView(DetailView):

        ...

        def get_context_data(self, **kwargs):
            context = super(MyView, self).get_context_data(self, **kwargs)
            context['meta'] = self.get_object().as_meta(self.request)
            return context

#. For Function Based View can just use ``as_meta()`` method for pass "meta" context variable::

    def post(request, id):
        template = 'single_post.html'
        post = Post.objects.get(pk=id)
        context = {}
        context['post'] = post
        context['meta'] = post.as_meta()
        return render(request, template, context)

#. Include ``meta/meta.html`` template in your templates::

    {% load meta %}

    <html>
    <head {% meta_namespaces %}>
        {% include "meta/meta.html" %}
    </head>
    <body>
    </body>
    </html>

Note
++++

* For OpenGraph / Facebook support, edit your ``<head>`` tag to use ``meta_namespaces`` templatetags

Reference template
------------------

See below the basic reference template::

    {% load meta %}

    <html>
    <head {% meta_namespaces %}>
        {% include "meta/meta.html" %}
    </head>
    <body>
    {% block content %}
    {% endblock content %}
    </body>
    </html>
