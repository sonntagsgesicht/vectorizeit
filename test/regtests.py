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

pkg = __import__(basename(getcwd()))


# first run will build reference values (stored in files)
# second run will test against those reference values
# to update reference values simply remove the according files

class FirstRegTests(RegressionTestCase):

    def test_sample_almost_equal(self):
        for i in range(-10, 100):
            self.assertAlmostRegressiveEqual(pkg.Line(0, 1).y(x=0.5 * i))

    def test_sample_equal(self):
        for i in range(-10, 100):
            self.assertAlmostRegressiveEqual(0 < pkg.Line(0, 1).y(x=0.5 * i))
