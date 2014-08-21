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

from cygapt.test.case import TestCase;
from cygapt.test.mock_objects import MockGenerator;
from cygapt.test.mock_objects import ExpectationFailedException;

class MockObjectTest(TestCase):
    def testMockedMethodIsNeverCalled(self):
        mock = self.getMock(MockGenerator);
        self.assertTrue(isinstance(mock, MockGenerator));
        mock.generate.expects(self.never());
        MockGenerator.verify();
        mock.generate();
        try:
            MockGenerator.verify();
            self.fail(); 
        except ExpectationFailedException:
            pass;
        except Exception:
            raise;
        MockGenerator.cleanup(); 

    def testMockedMethodIsCalledAtLeastOnce(self):
        mock = self.getMock(MockGenerator);
        mock.generate.expects(self.atLeastOnce());
        try:
            MockGenerator.verify();
            self.fail();
        except ExpectationFailedException:
            pass;
        except Exception:
            raise;
        mock.generate();
        mock.generate();

    def testMockedMethodIsCalledOnce(self):
        mock = self.getMock(MockGenerator);
        mock.generate.expects(self.once());
        mock.generate();
        MockGenerator.verify();
        mock.generate();
        try:
            MockGenerator.verify();
            self.fail()
        except ExpectationFailedException:
            pass;
        except Exception:
            raise;
        MockGenerator.cleanup(); 

    def testMockedMethodIsCalledOnceWithParameter(self):
        mock = self.getMock(MockGenerator);
        mock.generate.expects(self.once())\
            .calledWith('something')\
        ;
        mock.generate('something');
        MockGenerator.verify();
        mock.generate('something');
        try:
            MockGenerator.verify();
            self.fail();
        except ExpectationFailedException:
            pass;
        except Exception:
            raise;
        MockGenerator.cleanup(); 

    def testMockedMethodIsCalledExactly(self):
        mock = self.getMock(MockGenerator);
        mock.generate.expects(self.exactly(2));
        mock.generate();
        try:
            MockGenerator.verify();
            self.fail();
        except ExpectationFailedException:
            pass;
        except Exception:
            raise;
        mock.generate();
        MockGenerator.verify();
        mock.generate();
        try:
            MockGenerator.verify();
            self.fail();
        except ExpectationFailedException:
            pass;
        except Exception:
            raise;
        MockGenerator.cleanup(); 

    def testStubbedException(self):
        mock = self.getMock(MockGenerator);
        mock.generate.expects(self.any())\
            .will(self.raiseException(Exception()))\
        ;
        try:
            mock.generate();
            self.fail();
        except Exception:
            pass;

    def testStubbedReturnValue(self):
        mock = self.getMock(MockGenerator);
        mock.generate.expects(self.any())\
            .will(self.returnValue('foo'))\
        ;
        self.assertEqual('foo', mock.generate());

    def testFunctionCallback(self):
        callback = lambda *args: 'pass' if ['foo', 'bar'] == list(args) else None;
        mock = self.getMock(MockGenerator);
        mock.generate.expects(self.any())\
            .will(self.returnCallback(callback))\
        ;
        ret = mock.generate('foo', 'bar');
        self.assertEqual('pass', ret);

    def testMockClassOnlyGeneratedOnce(self):
        mock1 = self.getMock(MockGenerator);
        mock2 = self.getMock(MockGenerator);
        self.assertEqual(mock1.__class__.__name__, mock2.__class__.__name__);

    def testStubbedReturnValueMap(self):
        valueMap = [
            ('a', 'b', 'c', {}, 'd'),
            ('e', 'f', {'foo':'g'}, 'h'),
        ];
        mock = self.getMock(MockGenerator);
        mock.generate.expects(self.any())\
            .will(self.returnValueMap(valueMap))\
        ;
        self.assertEqual('d', mock.generate('a', 'b', 'c'));
        self.assertEqual('h', mock.generate('e', 'f', foo='g'));
        self.assertTrue(None is mock.generate('foo', 'bar'));


if '__main__' == __name__:
    unittest.main();
