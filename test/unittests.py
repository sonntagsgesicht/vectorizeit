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


pkg = __import__(basename(getcwd()))


class FirstUnitTests(TestCase):
    def setUp(self):
        pass

    def test_pkg_name(self):
        self.assertEqual(basename(getcwd()), pkg.__name__)

    def test_sample(self):
        self.assertEqual(1, pkg.Line(0, 1).y(x=1))
