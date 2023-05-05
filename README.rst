
.. image:: logo.png

Python Project *vectorize*
--------------------------

.. image:: https://github.com/sonntagsgesicht/vectorizeit/actions/workflows/python-package.yml/badge.svg
    :target: https://github.com/sonntagsgesicht/vectorizeit/actions/workflows/python-package.yml
    :alt: GitHubWorkflow

.. image:: https://img.shields.io/readthedocs/vectorizeit
   :target: http://vectorizeit.readthedocs.io
   :alt: Read the Docs

.. image:: https://img.shields.io/github/license/sonntagsgesicht/vectorizeit
   :target: https://github.com/sonntagsgesicht/vectorizeit/raw/master/LICENSE
   :alt: GitHub

.. image:: https://img.shields.io/github/release/sonntagsgesicht/vectorizeit?label=github
   :target: https://github.com/sonntagsgesicht/vectorizeit/releases
   :alt: GitHub release

.. image:: https://img.shields.io/pypi/v/vectorizeit
   :target: https://pypi.org/project/vectorizeit/
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/vectorizeit
   :target: https://pypi.org/project/vectorizeit/
   :alt: PyPI - Python Version

.. image:: https://pepy.tech/badge/vectorizeit
   :target: https://pypi.org/project/vectorizeit/
   :alt: PyPI Downloads


Introduction
------------

To import the project simply type

.. code-block:: python

    >>> from vectorizeit import vectorize

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

    $ pip install vectorizeit


License
-------

Code and documentation are available according to the license
(see LICENSE file in repository).
