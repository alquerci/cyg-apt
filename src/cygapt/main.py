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

from __future__ import print_function;
from __future__ import absolute_import;

import sys;
import os;

from cygapt.exception import ApplicationException;
from cygapt.app_container import AppContainer;

class CygAptMain():
    def __init__(self):
        self.__appName = None;
        try:
            exit_code = self.main();
        except ApplicationException as e:
            print("{0}: {1}".format(self.getAppName(), e),
                  file=sys.stderr
            );
            exit_code = e.getCode();

        sys.exit(exit_code);

    def getAppName(self):
        if self.__appName is None:
            self.__appName = os.path.basename(sys.argv[0]);
            if (self.__appName[-3:] == ".py"):
                self.__appName = self.__appName[:-3];
        return self.__appName;

    def main(self):
        container = AppContainer();

        argParser = container.get('arg_parser');
        input_ = argParser.parse();

        app = container.get('application');

        return app.run(input_);

if __name__ == '__main__':
    CygAptMain();
