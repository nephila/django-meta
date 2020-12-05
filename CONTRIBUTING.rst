############
Contributing
############

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
**********************

Report Bugs
===========

Report bugs at https://github.com/nephila/django-meta/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
========

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
==================

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

Write Documentation
===================

django-meta could always use more documentation, whether as part of the
official django-meta docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
===============

The best way to send feedback is to file an issue at https://github.com/nephila/django-meta/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

************
Get Started!
************

Ready to contribute? Here's how to set up ``django-meta`` for local development.

1. Fork the ``django-meta`` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/django-meta.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper
   installed, this is how you set up your fork for local development::

    $ mkvirtualenv django-meta
    $ cd django-meta/
    $ pip install -r requirements-test.txt
    $ pip install -e .

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the
tests, including testing other Python versions with tox::

    $ tox

To get tox, pip install it into your virtualenv.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Development tips
----------------

This project allows you to use `pre-commit <https://pre-commit.com/>`_ to ensure an easy compliance
to the project code styles.

If you want to use it, install it globally (for example with ``pip3 install --user precommit``,
but check `installation instruction <https://pre-commit.com/#install>`.
When first cloning the project ensure you install the git hooks by running ``pre-commit install``.

From now on every commit will be checked against our code style.

Check also the available tox environments with ``tox -l``: the ones not marked with a python version number are tools
to help you work on the project buy checking / formatting code style, running docs etc.

Testing tips
----------------
You can test your project using any specific combination of python, django and django cms.

For example ``tox -py37-django30-cms37`` runs the tests on python 3.7, Django 3.0 and django CMS 3.7.

As the project uses `pytest <https://pytest.org/>`_ as test runner, you can pass any pytest option by setting the
``PYTEST_ARGS`` environment variable, usually by prepending to the ``tox`` command. Example::

    PYTEST_ARGS=" -s  tests/test_plugins.py::PluginTest -p no:warnings" tox -py37-django30-cms37


Pull Request Guidelines
=======================

Before you submit a pull request, check that it meets these guidelines:

#. Pull request must be named with the following naming scheme:

   ``<type>/(<optional-task-type>-)<number>-description``

   See below for available types.

#. The pull request should include tests.
#. If the pull request adds functionality, the docs should be updated.
   Documentation must be added in ``docs`` directory, and must include usage
   information for the end user.
   In case of public API method, add extended docstrings with full parameters
   description and usage example.
#. Add a changes file in ``changes`` directory describing the contribution in
   one line. It will be added automatically to the history file upon release.
   File must be named as ``<issue-number>.<type>`` with type being:

   * ``.feature``: For new features.
   * ``.bugfix``: For bug fixes.
   * ``.doc``: For documentation improvement.
   * ``.removal``: For deprecation or removal of public API.
   * ``.misc``: For general issues.

   Check `towncrier`_ documentation for more details.

#. The pull request should work for all python / django / django CMS versions
   declared in tox.ini.
   Check the CI and make sure that the tests pass for all supported versions.

Release a version
=================

#. Update authors file
#. Merge ``develop`` on ``master`` branch
#. Bump release via task: ``inv tag-release (major|minor|patch)``
#. Update changelog via towncrier: ``towncrier --yes``
#. Commit changelog with ``git commit --amend`` to merge with bumpversion commit
#. Create tag ``git tag <version>``
#. Push tag to github
#. Publish the release from the tags page
#. If pipeline succeeds, push ``master``
#. Merge ``master`` back on ``develop``
#. Bump developement version via task: ``inv tag-dev -l (major|minor|patch)``
#. Push ``develop``

.. _towncrier: https://pypi.org/project/towncrier/#news-fragments
