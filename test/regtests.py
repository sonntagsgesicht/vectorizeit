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
from os.path import basename, split
from regtest import RegressionTestCase

from vectorize import vectorize


# first run will build reference values (stored in files)
# second run will test against those reference values
# to update reference values simply remove the according files

class VectorizeRegTests(RegressionTestCase):
    compression = False

    def test_vectorize_function(self):
        # disabled due to json tuple2list issue in regtest

        @vectorize(keys=['a'], types=(tuple, list,), returns=list)
        def test(a, b, c=None, *args, **kwargs):
            r = a, b, c, args, kwargs
            # print(*r)
            return r

        rng = range(10)
        lst = list(rng)

        t = test(lst, [2, 9], c=[3, 4], d=[6, 7])
        self.assertRegressiveEqual(t)

    def test_vectorize_method(self):
        # disabled due to json tuple2list issue in regtest

        class Test(list):

            @vectorize(['item'], returns=list)
            def __getitem__(self, item):
                return super().__getitem__(item)

        t = Test(range(10, -10, -1))
        self.assertRegressiveEqual(t[1])
        self.assertRegressiveEqual([t[1]])
        self.assertRegressiveEqual(t[(1, 3, 5)])

    def test_vectorize_zipped(self):
        # disabled due to json tuple2list issue in regtest

        @vectorize(keys=('a', 'b', 'c', 'd'), returns=list, zipped=True)
        def test_zipped(a, b, c=None, *args, **kwargs):
            r = a, b, c, args, kwargs
            # print(*r)
            return r

        rng = range(10)
        lst = list(rng)

        t = test_zipped(lst, [2, 3, 4, 0], c=[3, 4, 6, 7], d=['a', 'b', 'c'])
        self.assertRegressiveEqual(t)

    def test_vectorize_tensor(self):
        # disabled due to json tuple2list issue in regtest

        @vectorize(keys=('b', 'c', 'd'))
        def test_tensorized(a, b, c=None, *args, **kwargs):
            r = a, b, c, args, kwargs
            # print(*r)
            return r

        rng = range(10)
        lst = list(rng)

        t = test_tensorized(lst, [2, 3, 4], c=[3, 4, 6, 7], d=['a', 'b', 'c'])
        self.assertRegressiveEqual(t)

        t = test_tensorized(lst, '56', c=[3, 4, 5, 7], d=['a', 'b', 'c'])
        self.assertRegressiveEqual(t)

        t = test_tensorized(lst, '56', c='hello', d=['a', 'b', 'c'])
        self.assertRegressiveEqual(t)

        t = test_tensorized(lst, '56', 'hello', (123, 321), d=['a', 'b', 'c'])
        self.assertRegressiveEqual(t)

        t = test_tensorized(lst, (123, 321), d=['a', 'b', 'c'])
        self.assertRegressiveEqual(t)

        t = test_tensorized(lst, (123, 345), 321, d='c')
        self.assertRegressiveEqual(t)

        t = test_tensorized(lst, 123, 321, d='c')
        self.assertRegressiveEqual(t)
