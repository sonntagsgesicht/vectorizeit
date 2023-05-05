
.. image:: logo.png

Python Project *vectorize*
--------------------------

.. image:: https://github.com/sonntagsgesicht/vectorize/actions/workflows/python-package.yml/badge.svg
    :target: https://github.com/sonntagsgesicht/vectorize/actions/workflows/python-package.yml
    :alt: GitHubWorkflow

.. image:: https://img.shields.io/readthedocs/vectorize
   :target: http://vectorize.readthedocs.io
   :alt: Read the Docs

.. image:: https://img.shields.io/github/license/sonntagsgesicht/vectorize
   :target: https://github.com/sonntagsgesicht/vectorize/raw/master/LICENSE
   :alt: GitHub

.. image:: https://img.shields.io/github/release/sonntagsgesicht/vectorize?label=github
   :target: https://github.com/sonntagsgesicht/vectorize/releases
   :alt: GitHub release

.. image:: https://img.shields.io/pypi/v/vectorize
   :target: https://pypi.org/project/vectorize/
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/vectorize
   :target: https://pypi.org/project/vectorize/
   :alt: PyPI - Python Version

.. image:: https://pepy.tech/badge/vectorize
   :target: https://pypi.org/project/vectorize/
   :alt: PyPI Downloads


Introduction
------------

To import the project simply type

.. code-block:: python

    >>> from vectorize import vectorize

after installation and use **vectorize** as a decorator
to iterate over arguments of list type.

.. code-block:: python

    >>> @vectorize(keys=['a', 'b'])
    ... def foo(a, b):
    ...     return a, b

    >>> foo((1, 2), ['a', 'b'])
    (((1, 'a'), (1, 'b')), ((2, 'a'), (2, 'b')))


Install
-------

The latest stable version can always be installed or updated via pip:

.. code-block:: bash

    $ pip install vectorize


License
-------

Code and documentation are available according to the license
(see LICENSE file in repository).
