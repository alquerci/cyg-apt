#!/usr/bin/python
######################## BEGIN LICENSE BLOCK ########################
# This file is part of the cygapt package.
#
# Copyright (C) 2002-2009 Jan Nieuwenhuizen  <janneke@gnu.org>
#               2002-2009 Chris Cormie       <cjcormie@gmail.com>
#                    2012 James Nylen        <jnylen@gmail.com>
#               2012-2013 Alexandre Quercia  <alquerci@email.com>
#
# For the full copyright and license information, please view the
# LICENSE file that was distributed with this source code.
######################### END LICENSE BLOCK #########################

from __future__ import print_function;
from __future__ import absolute_import;

import unittest;

from cygapt.test.test_utils import TestUtils;
from cygapt.test.test_url_opener import TestUrlOpener;
from cygapt.test.test_ob import TestOb;
from cygapt.test.test_path_mapper import TestPathMapper;
from cygapt.test.test_setup import TestSetup;
from cygapt.test.test_cygapt import TestCygApt as TestCygAptClass;

class TestCygApt(unittest.TestSuite):
    def __init__(self):
        loader = unittest.TestLoader();
        self.addTests(
            loader.loadTestsFromTestCase(TestUtils),
            loader.loadTestsFromTestCase(TestUrlOpener),
            loader.loadTestsFromTestCase(TestOb),
            loader.loadTestsFromTestCase(TestPathMapper),
            loader.loadTestsFromTestCase(TestSetup),
            loader.loadTestsFromTestCase(TestCygAptClass),
        );

if __name__ == "__main__":
    unittest.main();
