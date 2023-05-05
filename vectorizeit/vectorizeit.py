# -*- coding: utf-8 -*-

# vectorizeit
# -----------
# simply vectorize Python functions and methods by iteration.
#
# Author:   sonntagsgesicht
# Version:  0.1.2, copyright Friday, 05 May 2023
# Website:  https://github.com/sonntagsgesicht/vectorizeit
# License:  Apache License 2.0 (see LICENSE file)


from functools import wraps
from inspect import getargs

ITERABLES = list, tuple, set, dict


def vectorize(keys=(), types=None, returns=None, zipped=False):
    """simply vectorize Python functions and methods by iteration.

    :param keys: set **keys** to identify arguments to iterate
        by default no argument is vectorized
    :param types: only arguments of types as specified in **types**
        will be vectorized.
        If not spefivied this defaults
        to **list**, **tuple**, **set** and **dict**.
    :param returns: the type of return value is set by **returns**
        by default the return value has the same type
        as the vectorized argument.
        If set to **'none'** no value ist returned.
        Only if **zipped** is **True** the default return type is **tuple**.
    :param zipped: if multiple arguments are vectors **zipped** sets the way
        to iterate,
        either - by default - tensor-like, i.e. one argumnet after the other
        which resuts in nested vectors,
        or as **zipped** is **True** by iterating of all vector argunments
        in parallel and at once.

    Simply use the decorator to vectorize a function.

    >>> from vectorizeit import vectorize

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

    In order to avoid unexcpected vectorization one can fix
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

    """  # noqa E501
    types = types or ITERABLES
    none_return = returns == 'none'
    returns = tuple if none_return else returns

    def decorator(func):
        args_list, _, _ = getargs(func.__code__)
        args_index = [args_list.index(k) for k in keys if k in args_list]

        def _update(item, k, v):
            if not isinstance(k, list):
                item[k] = v
            else:
                for kk, vv in zip(k, v):
                    item[kk] = vv
            return item

        @wraps(func)
        def do(*args, **kwargs):
            args_indexes = [i for i in args_index if
                            i < len(args) and isinstance(args[i], types)]
            if not zipped and args_indexes:
                args = list(args)
                index = args_indexes[0]
                cls = returns or args[index].__class__
                ret = cls(do(*_update(args, index, a), **kwargs)
                          for a in args[index])
                return None if none_return else ret

            vargs_indexes = [i for i in range(len(args_list), len(args)) if
                             isinstance(args[i], types)]
            if not zipped and vargs_indexes:
                args = list(args)
                index = vargs_indexes[0]
                cls = returns or args[index].__class__
                ret = cls(do(*_update(args, index, a), **kwargs)
                          for a in args[index])
                return None if none_return else ret

            kwargs_keys = [k for k in keys if
                           k in kwargs and isinstance(kwargs[k], types)]
            if not zipped and kwargs_keys:
                key = kwargs_keys[0]
                cls = returns or kwargs[key].__class__
                ret = cls(do(*args, **_update(kwargs, key, k))
                          for k in kwargs[key])
                return None if none_return else ret

            if zipped and (args_indexes or vargs_indexes or kwargs_keys):
                # build args/kwargs vector lists to zip
                args_vec = [args[i] for i in args_indexes]
                vargs_vec = [args[i] for i in vargs_indexes]
                kwargs_vec = [kwargs[k] for k in kwargs_keys]

                # zip args/kwargs to single list of dicts
                nargs = [_update(list(args), args_indexes, row)
                         for row in zip(*args_vec)]
                nargs += [_update(list(args), vargs_indexes, row)
                          for row in zip(*vargs_vec)]
                nkwargs = [_update(dict(kwargs), kwargs_keys, row)
                           for row in zip(*kwargs_vec)]

                # update(args/kwargs) to invoke func
                cls = returns or tuple
                ret = cls(func(*na, **nkw) for na, nkw in zip(nargs, nkwargs))
                return ret
                return None if none_return else ret

            return func(*args, **kwargs)

        return do
    return decorator
