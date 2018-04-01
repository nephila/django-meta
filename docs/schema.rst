.. _schema.org:

**********
schema.org
**********

``django-meta`` provides full support for schema.org in JSON-LD format.

schema.org is supported in both :ref:`models` and :ref:`views` framework.

Model-level
-----------

In the same way as basic :py:attr:`~meta.models.ModelMeta._metadata` attribute,
:py:attr:`~meta.models.ModelMeta._schema` exists to resolve and build
the per-object **Schema.org** representation of the current object.

As per :py:attr:`~meta.models.ModelMeta._metadata`, :py:attr:`~meta.models.ModelMeta._schema`
values can contains the name of a method, property or attribute available on the class:

.. _schema.model:

.. code-block:: python

    class Blog(ModelMeta, Model)
        ...
        _schema = {
            'image': 'get_image_full_url',
            'articleBody': 'text',
            'articleSection': 'get_categories',
            'author': 'get_schema_author',
            'copyrightYear': 'copyright_year',
            'dateCreated': 'get_date',
            'dateModified': 'get_date',
            'datePublished': 'date_published',
            'headline': 'headline',
            'keywords': 'get_keywords',
            'description': 'get_description',
            'name': 'title',
            'url': 'get_full_url',
            'mainEntityOfPage': 'get_full_url',
            'publisher': 'get_site',
        }



View-level
----------

:py:class:`~meta.views.Meta` and :py:class:`~meta.views.MetadataMixin` provides a few API to work with **schema.org**
properties.

.. _schema.get_schema:

MetadataMixin
+++++++++++++

The high level interface is :py:meth:`meta.views.MetadataMixin.get_schema` which works in much the same way as
:py:attr:`meta.models.ModelMeta._schema`.

In :py:meth:`~meta.views.MetadataMixin.get_schema` you must return the whole **schema.org** structure.

For a single object it can look like this:

.. code-block:: python

    def get_schema(self, context=None):
        return {
            'image': self.object.get_image_full_url(),
            'articleBody': self.object.text,
            'articleSection': self.object.get_categories(),
            'author': self.object.get_schema_author(),
            'copyrightYear': self.object.date_published.year,
            'dateCreated': self.object.get_date(),
            'dateModified': self.object.get_date(),
            'datePublished': self.object.date_published(),
            'headline': self.object.abstract[:50],
            'keywords': self.object.get_keywords(),
            'description': self.object.get_description(),
            'name': self.object.title(),
            'url': self.object.get_full_url(),
            'mainEntityOfPage': self.object.get_full_url(),
            'publisher': self.object.get_site(),
        }


.. note:: as it's :py:attr:`~meta.views.Meta.schema` responsibility to convert objects to types suitable for json encoding,
          you are not required to put only literal values here. Instances of :py:class:`~meta.views.Meta`, dates, iterables
          and dictionaries are allowed.

.. _schema._schema:

Meta
++++

The low level interface is :py:meth:`meta.views.Meta._schema` attribute or (``schema`` argument to :py:class:`~meta.views.Meta`
constructor):

.. code-block:: python

    class MyView(View):

        def get_context_data(self, **kwargs):
            context = super(PostDetailView, self).get_context_data(**kwargs)
            context['meta'] = Meta(schema={
                '@type': 'Organization',
                'name': 'My Publisher',
                'logo': Meta(schema={
                    '@type': 'ImageObject',
                    'url': self.get_image_full_url()
                })
            })
            return context
