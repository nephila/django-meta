# -*- coding: utf-8 -*-
from setuptools import setup
import meta

setup(
    name='django-meta',
    description='Pluggable app for handling webpage meta tags and OpenGraph '
                'properties',
    long_description=open('README.rst').read(),
    version=meta.__version__,
    packages=['meta', 'meta.templatetags', 'meta_mixin'],
    package_data={
        'meta': ['templates/*.html', 'templates/meta_mixin/*.html', 'templates/meta/*.html'],
    },
    author='Monwara LLC',
    maintainer='Nephila',
    author_email='branko@monwara.com',
    maintainer_email='info@nephila.it',
    url='https://github.com/nephila/django-meta',
    license='BSD',
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
