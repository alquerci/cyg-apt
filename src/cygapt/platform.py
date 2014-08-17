# -*- coding: utf-8 -*-
# This file is part of the cygapt package.
#
# (c) Alexandre Quercia <alquerci@email.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.

from __future__ import absolute_import;

import os;
import sys;
import platform;

"""
"""

class Platform():
    def __init__(self):
        self.__appName = None;

    def getAppName(self):
        if None is not self.__appName :
            return self.__appName;

        self.__appName = os.path.basename(sys.argv[0]);
        if (self.__appName[-3:] == ".py"):
            self.__appName = self.__appName[:-3];

        return self.__appName;

    def isCygwin(self):
        return sys.platform.startswith('cygwin');

    def getArchitecture(self):
        arch = "x86";

        if "x86_64" == platform.machine() :
            arch = "x86_64";

        return arch;
