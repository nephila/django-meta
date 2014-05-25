from distutils.core import setup

setup(
    name='django-meta',
    description='Pluggable app for handling webpage meta tags and OpenGraph '
    'properties',
    long_description=open('README.rst').read(),
    version='0.1.0',
    packages=['meta', 'meta.templatetags'],
    package_data={
        'meta': ['templates/*.html'],
    },
    author='Monwara LLC',
    maintainer='Nephila',
    author_email='branko@monwara.com',
    maintainer_email='info@nephila.it',
    url='https://github.com/nephila/django-meta',
    license='BSD',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
    ],
)


