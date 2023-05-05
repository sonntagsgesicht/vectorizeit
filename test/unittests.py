# -*- coding: utf-8 -*-

# auxilium
# --------
# A Python project for an automated test and deploy toolkit - 100%
# reusable.
#
# Author:   sonntagsgesicht
# Version:  0.1.4, copyright Sunday, 11 October 2020
# Website:  https://github.com/sonntagsgesicht/auxilium
# License:  Apache License 2.0 (see LICENSE file)


from os import getcwd
from os.path import basename
from unittest import TestCase


from vectorizeit import vectorize


class VectorizeUnitTests(TestCase):

    def test_vectorize_function(self):

        @vectorize(keys=['a'], types=(tuple, list,), returns=list)
        def test(a, b, c=None, *args, **kwargs):
            r = a, b, c, args, kwargs
            # print(*r)
            return len(str(r))

        rng = range(10)
        lst = list(rng)

        t = test(lst, [2, 9], c=[3, 4], d=[6, 7])
        self.assertTrue(isinstance(t, list))
        self.assertEqual(10, len(t))

        t = test(rng, [2, 9], c=[3, 4], d=[6, 7])
        self.assertTrue(isinstance(t, int))
        self.assertEqual(49, t)

    def test_vectorize_method(self):

        class Test(list):

            @vectorize(['item'], returns=list)
            def __getitem__(self, item):
                return super().__getitem__(item)

        t = Test(range(10, -10, -1))
        self.assertEqual(9, t[1])
        self.assertEqual([9], [t[1]])
        self.assertEqual([9, 7, 5], t[(1, 3, 5)])

    def test_vectorize_zipped(self):

        @vectorize(keys=('a', 'b', 'c', 'd'), returns=list, zipped=True)
        def test_zipped(a, b, c=None, *args, **kwargs):
            r = a, b, c, args, kwargs
            # print(*r)
            return len(str(r))

        rng = range(10)
        lst = list(rng)

        t = test_zipped(lst, [2, 3, 4, 0], c=[3, 4, 6, 7], d=['a', 'b', 'c'])
        self.assertTrue(isinstance(t, list))
        self.assertEqual(3, len(t))

    def test_vectorize_tensor(self):

        @vectorize(keys=('b', 'c', 'd'))
        def test_tensorized(a, b, c=None, *args, **kwargs):
            r = a, b, c, args, kwargs
            # print(*r)
            return len(str(r))

        rng = range(10)
        lst = list(rng)

        t = test_tensorized(lst, [2, 3, 4], c=[3, 4, 6, 7], d=['a', 'b', 'c'])
        self.assertTrue(isinstance(t, list))
        self.assertEqual(3, len(t))

        t = test_tensorized(lst, '56', c=[3, 4, 5, 7], d=['a', 'b', 'c'])
        self.assertTrue(isinstance(t, list), type(t))
        self.assertEqual(4, len(t))

        t = test_tensorized(lst, '56', c='hello', d=['a', 'b', 'c'])
        self.assertTrue(isinstance(t, list))
        self.assertEqual(3, len(t))

        t = test_tensorized(lst, '56', 'hello', (123, 321), d=['a', 'b', 'c'])
        self.assertTrue(isinstance(t, tuple))
        self.assertEqual(2, len(t))

        t = test_tensorized(lst, (123, 321), d=['a', 'b', 'c'])
        self.assertTrue(isinstance(t, tuple))
        self.assertEqual(2, len(t))

        t = test_tensorized(lst, {123, 321}, d=('a', 'b', 'c'))
        # d must be tuple as a set is not hashable
        # hence only the frist entry may be a set
        # as sets are not hashable either
        self.assertTrue(isinstance(t, set))
        self.assertEqual(1, len(t))  # as test2 returns always the same value

        t = test_tensorized(rng, (123, 345), 321, d='c')
        self.assertTrue(isinstance(t, tuple))
        self.assertEqual(2, len(t))

        t = test_tensorized(rng, 123, 321, d='c')
        self.assertTrue(isinstance(t, int))
        self.assertEqual(40, t)

    def test_vectorize_none(self):
        @vectorize(keys=['a'], types=(tuple, list,), returns='none')
        def test(a, b, c=None, *args, **kwargs):
            r = a, b, c, args, kwargs
            # print(*r)
            return len(str(r))

        rng = range(10)
        lst = list(rng)

        t = test(lst, [2, 9], c=[3, 4], d=[6, 7])
        self.assertTrue(t is None)

        t = test(rng, [2, 9], c=[3, 4], d=[6, 7])
        self.assertTrue(isinstance(t, int))
        self.assertEqual(49, t)
