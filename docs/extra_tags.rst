.. _extra_tags:

Adding custom tags / properties
===============================

Both :ref:`models <models>` and :ref:`views <views>` support adding custom tags
and properties by extending the respective python classes.

They both rely on the following attributes:

* ``extra_props``: use this to add new meta tags using the ``name`` attribute as key. Example:

      .. code-block:: html

         <meta name="designer" content="Pablo Picasso">


* ``extra_custom_props``: use this to add new meta tags using a custom attribute as key. Example:

      .. code-block:: html

         <meta property="og:type" content="music.song" />
         <meta property="music:duration" content="3" />

Using this approach, you won't need to change the ``meta.html`` template to include your custom tags.

See below concrete implementation examples.

Format
--------

extra_props
~~~~~~~~~~~~~

A dictionary of extra optional properties:

.. code-block:: python

    {
        'foo': 'bar',
        'key': 'value'
    }

.. code-block:: html

    <meta name="foo" content="bar">
    <meta name="key" content="value">

extra_custom_props
~~~~~~~~~~~~~~~~~~~

A list of tuples for rendering custom extra properties:

.. code-block:: python

    [
        ('key', 'foo', 'bar')
        ('property', 'name', 'value')
    ]

.. code-block:: html

    <meta name="foo" content="bar">
    <meta property="name" content="value">

.. _extra_tags_views:

Views
--------

To add custom tags / properties you can follow the same specifications detailed in :ref:`Using the view`.

* Pass the values to the ``Meta`` object (see :ref:`meta object`):

      .. code-block:: python

            meta = Meta(
               ...
                extra_props={
                    'designer': 'Pablo Picasso',
                },
                extra_custom_props=[
                    ('property', 'og:type', 'music.song'),
                    ('property', 'music:duration', '3')
                ]
                ...
            )


* add as attributes to the view using :py:class:`meta.views.MetadataMixin` (see :ref:`view mixin`):

      .. code-block:: python

            class MyView(MetadataMixin, ListView):
                ...
                extra_props = {
                    'designer': 'Pablo Picasso',
                }
                extra_custom_props = [
                    ('property', 'og:type', 'music.song'),
                    ('property', 'music:duration', '3')
                ]
                ...

.. _extra_tags_models:

Models
--------

For models they need to be added to the ``_metadata`` attribute as per the other properties (see :ref:`model_metadata`).

As the other properties you can both provide the static value (see ``extra_props`` below, or the name of a callable which will return the value at runtime (see ``extra_custom_props``).

.. code-block:: python

    class Post(ModelMeta, models.Model):
        ...
        _metadata = {
            ...
            'extra_props': {
                'designer': 'Pablo Picasso',
            },
            'extra_custom_props': 'get_custom_props'
        }
        ...
        def get_custom_props(self):
            return [
                ('property', 'og:type', 'music.song'),
                ('property', 'music:duration', '3')
            ]
        ...
