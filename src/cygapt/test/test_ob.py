#!/usr/bin/env python
# -*- coding: utf-8 -*-
######################## BEGIN LICENSE BLOCK ########################
# This file is part of the cygapt package.
#
# Copyright (C) 2002-2009 Jan Nieuwenhuizen  <janneke@gnu.org>
#               2002-2009 Chris Cormie       <cjcormie@gmail.com>
#                    2012 James Nylen        <jnylen@gmail.com>
#               2012-2014 Alexandre Quercia  <alquerci@email.com>
#
# For the full copyright and license information, please view the
# LICENSE file that was distributed with this source code.
######################### END LICENSE BLOCK #########################
"""
    unit test for cygapt.ob
"""

from __future__ import print_function;
from __future__ import absolute_import;

import unittest;
import sys;

from cygapt.test.case import TestCase;
from cygapt.ob import CygAptOb;

REPR_STDOUT = repr(sys.stdout);

class TestOb(TestCase):
    def setUp(self):
        TestCase.setUp(self);
        self.obj = CygAptOb(False);

    def tearDown(self):
        self.obj._end();
        TestCase.tearDown(self);

    def makeOn(self):
        txt = "TestOb.makeOn ";
        print(txt, end="");
        value = sys.stdout.getvalue();
        self.assertTrue(value.endswith(txt));
        self.assertTrue(self.obj._state);

    def makeOff(self):
        self.assertEqual(repr(sys.stdout), REPR_STDOUT);
        self.assertFalse(self.obj._state);

    def test__init__(self):
        self.assertTrue(isinstance(self.obj, CygAptOb));

    def testClean(self):
        self.obj.clean();
        self.makeOff();
        self.obj.start();
        self.makeOn();
        self.obj.clean();
        self.assertEqual(self.obj._buffer.getvalue(), "");
        self.assertNotEqual(self.obj._value, "");
        self.assertNotEqual(self.obj.getContents(), "");

    def testStartEnd(self):
        self.obj._end();
        self.makeOff();
        self.obj.start();
        self.makeOn();
        self.obj._end();
        self.makeOff();

    def testEndClean(self):
        self.obj.endClean();
        self.makeOff();
        self.obj.start();
        self.makeOn();
        self.obj.endClean();
        self.makeOff();

    def testEndFlush(self):
        self.obj.endFlush();
        self.makeOff();
        self.obj.start();
        self.makeOn();
        self.obj.endFlush();
        self.makeOff();

    def testFlush(self):
        self.obj.flush();
        self.makeOff();
        self.obj.start();
        self.makeOn();
        self.obj.flush();
        self.makeOn();

    def testGetClean(self):
        ret = self.obj.getClean();
        self.assertFalse(ret);
        self.makeOff();
        self.obj.start();
        self.makeOn();
        t = self.obj._buffer.getvalue();
        txt = "TestOb.test_getClean";
        print(txt);
        ret = self.obj.getClean();
        self.assertEqual(ret, "{0}{1}\n".format(t, txt));
        self.makeOff();

    def testGetContent(self):
        ret = self.obj.getContents();
        self.assertFalse(ret);
        self.makeOff();
        self.obj.start();
        txt = "TestOb.test_get_content";
        print(txt);
        ret = self.obj.getContents();
        self.assertEqual(ret, "{0}\n".format(txt));
        self.makeOn();

    def testGetFlush(self):
        ret = self.obj.getFlush();
        self.assertFalse(ret);
        self.makeOff();
        self.obj.start();
        txt = "TestOb.test_getFlush";
        print(txt);
        ret = self.obj.getFlush();
        self.assertEqual(ret, "{0}\n".format(txt));
        self.makeOff();

    def testGetLength(self):
        ret = self.obj.getLength();
        self.assertFalse(ret);
        self.makeOff();
        self.obj.start();
        length = 10;
        print("t" * length);
        ret = self.obj.getLength();
        self.assertEqual(ret, length + 1);
        self.makeOn();

    def testImplicitFlush(self):
        self.obj.implicitFlush(True);
        self.makeOff();
        self.obj.implicitFlush(False);
        self.makeOn();

if __name__ == "__main__":
    unittest.main();
