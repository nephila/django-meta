from distutils.core import setup

setup(
    name='django-meta',
    description='Pluggable app for handling webpage meta tags and OpenGraph '
    'properties',
    long_description=open('README.rst').read(),
    version='0.0.3',
    packages=['meta', 'meta.templatetags'],
    package_data={
        'meta': ['templates/*.html'],
    },
    author='Monwara LLC',
    author_email='branko@monwara.com',
    url='https://bitbucket.org/monwara/django-meta',
    download_url='https://bitbucket.org/monwara/django-meta/downloads',
    license='BSD',
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
    ],
)


