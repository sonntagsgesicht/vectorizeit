

.. doctest::

    >>> from vectorizeit import vectorize

    >>> @vectorize(keys=['a', 'b'])
    ... def foo(a, b):
    ...     return a, b

    >>> foo((1, 2), ('a', 'b'))
    (((1, 'a'), (1, 'b')), ((2, 'a'), (2, 'b')))

But there is more to explore. For instance, the return type is the same
as the vector argument type.

    >>> foo([1, 2], ['a', 'b'])
    [[(1, 'a'), (1, 'b')], [(2, 'a'), (2, 'b')]]

To flatten such tensor use

    >>> from itertools import chain
    >>> list(chain.from_iterable(foo([1, 2], ['a', 'b'])))
    [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]

Or even

    >>> @vectorize(keys=['b'])
    ... def foo(a, b, c=None, *args, **kwargs):
    ...     return a, b, c, args, kwargs

    >>> r = foo(1, ['b1', 'b2'], d=[10, 11])

    >>> type(r)
    <class 'list'>

    >>> r
    [(1, 'b1', None, (), {'d': [10, 11]}), (1, 'b2', None, (), {'d': [10, 11]})]

This works also with multiple arguments and multiple vector inputs.

    >>> @vectorize(keys=['b', 'c'])
    ... def foo(a, b, c=None, *args, **kwargs):
    ...     return a, b, c, args, kwargs

    >>> foo(1, ['b1', 'b2'], c=(1, 2), d=[10, 11])
    [((1, 'b1', 1, (), {'d': [10, 11]}), (1, 'b1', 2, (), {'d': [10, 11]})), ((1, 'b2', 1, (), {'d': [10, 11]}), (1, 'b2', 2, (), {'d': [10, 11]}))]

Setting the **zipped** decorator argument will iter in parallel
over the mutiple vector inputs as have been zipped.

    >>> @vectorize(keys=['b', 'c'], zipped=True)
    ... def foo(a, b, c=None, *args, **kwargs):
    ...     return a, b, c, args, kwargs

    >>> foo(1, ['b1', 'b2'], c=(1, 2), d=[10, 11])
    ((1, 'b1', 1, (), {'d': [10, 11]}), (1, 'b2', 2, (), {'d': [10, 11]}))

To fix the return value type set **returns**.

    >>> @vectorize(keys=['b', 'c'], returns=list)
    ... def foo(a, b, c=None, *args, **kwargs):
    ...     return a, b, c, args, kwargs

    >>> foo(1, ['b1', 'b2'], d=[10, 11])
    [(1, 'b1', None, (), {'d': [10, 11]}), (1, 'b2', None, (), {'d': [10, 11]})]

In order to avoid unexpected vectorization one can fix
specific types to be vectorized by setting **types**.

    >>> @vectorize(keys=['b', 'c'], types=(list,))
    ... def foo(a, b, c=None, *args, **kwargs):
    ...     return a, b, c, args, kwargs

    >>> foo(1, ['b1', 'b2'], d=[10, 11])
    [(1, 'b1', None, (), {'d': [10, 11]}), (1, 'b2', None, (), {'d': [10, 11]})]

    >>> foo(1, ('b1', 'b2'), d=[10, 11])
    (1, ('b1', 'b2'), None, (), {'d': [10, 11]})

vectorize works for methods, too.

    >>> class vector(list):
    ...
    ...    @vectorize(keys=['item'])
    ...    def __getitem__(self, item):
    ...        return super().__getitem__(item)

    >>> v = vector(range(3))
    >>> v
    [0, 1, 2]

    >>> v[(2, 1)]
    (2, 1)

And to be more careful use a custom class to control vectorization.

    >>> @vectorize(keys=['b', 'c'], types=(vector,))
    ... def foo(a, b, c=None, *args, **kwargs):
    ...     return a, b, c, args, kwargs

    >>> foo(1, ['b1', 'b2'], d=[10, 11])
    (1, ['b1', 'b2'], None, (), {'d': [10, 11]})

    >>> foo(1, vector(('b1', 'b2')), d=[10, 11])
    [(1, 'b1', None, (), {'d': [10, 11]}), (1, 'b2', None, (), {'d': [10, 11]})]
