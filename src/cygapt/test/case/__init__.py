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

from __future__ import absolute_import;

import sys;
import warnings;
from difflib import unified_diff as diff;

if sys.version_info < (3, ):
    from .py2 import TestCase as BaseTestCase;
else:
    from unittest import TestCase as BaseTestCase;

class TestCase(BaseTestCase):
    """Base class for all cygapt test case.
    """

    def assertEqual(self, expected, actual, message=""):
        """Asserts that two variables are equal.

        @param expected: mixed
        @param actual:   mixed
        @param message:  str

        @raise AssertionError: When the assertion failed
        """
        assert isinstance(message, str);

        try:
            BaseTestCase.assertEqual(self, expected, actual, message);
        except self.failureException :
            if not (isinstance(expected, str) and isinstance(actual, str)) :
                raise;
        else:
            return;

        if not message :
            message = "Failed asserting that two strings are equal.";

        message = "\n".join([message, "".join(list(diff(
            expected.splitlines(True),
            actual.splitlines(True),
            fromfile='Expected',
            tofile='Actual',
        )))]);

        raise self.failureException(message);

    def _assertDeprecatedWarning(self, message, callback, *args, **kwargs):
        """Asserts that a warning of type "DeprecationWarning" is triggered with message.

        When invoked the callback with arguments args and keyword arguments
        kwargs.

        @param message:  str      The expected warning message
        @param callback: callable The callback to call
        @param *args:    mixed
        @param **kwargs: mixed
        """
        assert isinstance(message, str);
        assert hasattr(callback, '__call__');

        with warnings.catch_warnings(record=True) as warnList :
            # cause all DeprecationWarning to always be triggered
            warnings.simplefilter("always", DeprecationWarning);

            # trigger a warning
            ret = callback(*args, **kwargs);

            # verify some things
            if not warnList :
                self.fail(" ".join([
                    "Failed asserting that a warning of type",
                    '"DeprecationWarning" is triggered',
                ]));

            messages = list();
            for warn in warnList :
                messages.append(str(warn.message));
                if message in messages[-1] :
                    return ret;

            self.fail("\n".join([
                "Failed asserting that at least one of these warning messages:",
                "{0}",
                "contains",
                "{1}",
            ]).format("\n".join(messages), message));

        return ret;

    def _assertNotDeprecatedWarning(self, message, callback, *args, **kwargs):
        """Asserts that a warning of type "DeprecationWarning" is not triggered with message.

        When invoked the callback with arguments args and keyword arguments
        kwargs.

        @param message:  str      The expected warning message
        @param callback: callable The callback to call
        @param *args:    mixed
        @param **kwargs: mixed
        """
        try:
            self._assertDeprecatedWarning(message, callback, *args, **kwargs);
        except self.failureException :
            return;

        self.fail(" ".join([
            "Failed asserting that a warning of type",
            '"DeprecationWarning" with message "{0}" is not triggered',
        ]).format(message));
