# -*- coding: utf-8 -*-
# This file is part of the cygapt package.
#
# (c) 2002-2009 Jan Nieuwenhuizen <janneke@gnu.org>
#     2002-2009 Chris Cormie      <cjcormie@gmail.com>
#          2012 James Nylen       <jnylen@gmail.com>
#     2012-2014 Alexandre Quercia <alquerci@email.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.

from __future__ import absolute_import;

import unittest;
import cygapt.test;

class TestCase(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self);
        cygapt.test.mock_objects.MockGenerator.cleanup();

    def tearDown(self):
        cygapt.test.mock_objects.MockGenerator.verify();
        unittest.TestCase.tearDown(self);

    def getMock(self, classType):
        return cygapt.test.mock_objects.MockGenerator.generate(classType);

    def any(self):
        return cygapt.test.mock_objects.AnyInvokedCountMatcher();

    def never(self):
        return cygapt.test.mock_objects.InvokedCountMatcher(0);

    def atLeastOnce(self):
        return cygapt.test.mock_objects.InvokedAtLeastOnceMatcher();

    def once(self):
        return cygapt.test.mock_objects.InvokedCountMatcher(1);

    def exactly(self, count):
        return cygapt.test.mock_objects.InvokedCountMatcher(count);

    def returnValue(self, value):
        return cygapt.test.mock_objects.ReturnStub(value);

    def returnValueMap(self, valueMap):
        return cygapt.test.mock_objects.ReturnValueMapStub(valueMap);

    def returnArgument(self, argumentIndex):
        return cygapt.test.mock_objects.ReturnArgumentStub(argumentIndex);

    def returnCallback(self, callback):
        return cygapt.test.mock_objects.ReturnCallbackStub(callback);

    def raiseException(self, exception):
        return cygapt.test.mock_objects.ExceptionStub(exception);
