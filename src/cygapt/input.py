# -*- coding: utf-8 -*-
# This file is part of the cygapt package.
#
# (c) Alexandre Quercia <alquerci@email.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.

from __future__ import absolute_import;

"""
"""

class Input():
    def __init__(self):
        self.__arguments = dict();
        self.__options = dict();

    def getArguments(self):
        return self.__arguments;

    def getArgument(self, name):
        return self.__arguments[name];

    def setArgument(self, name, value):
        self.__arguments[name] = value;

    def hasArgument(self, name):
        return self.__arguments.has_key(name);

    def getOptions(self):
        return self.__options;

    def getOption(self, name):
        return self.__options[name];

    def setOption(self, name, value):
        self.__options[name] = value;

    def hasOption(self, name):
        return self.__options.has_key(name);

    def __getattr__(self, name):
        if self.hasArgument(name) :
            return self.getArgument(name);

        if self.hasOption(name) :
            return self.getOption(name);
