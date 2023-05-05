
.. image:: logo.png


Python Project *vectorize*
-----------------------------------------------------------------------


Introduction
------------

To import the project simply type

.. code-block:: python

    >>> from vectorize import vectorize

after installation and use |vectorize| as a decorator
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
