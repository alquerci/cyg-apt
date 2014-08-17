# -*- coding: utf-8 -*-
# This file is part of the pymfony package.
#
# (c) Alexandre Quercia <alquerci@email.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.

from __future__ import absolute_import;

import os;
import re;

from cygapt.structure import ConfigStructure;
from cygapt.platform import Platform;

"""
"""

class Configuration():
    def __init__(self, platform):
        assert isinstance(platform, Platform);

        self.__rc = ConfigStructure();
        self.__platform = platform;
        self.__parsed = False;
        self.__path = None;

    def get(self, name):
        if not self.__parsed :
            self.__parse(self.getPath());

        return self.__rc.__dict__[name];

    def set(self, name, value):
#        self.__rc.__dict__[name] = value;
        setattr(self.__rc, name, value);

    def getConfig(self):
        if not self.__parsed :
            self.__parse(self.getPath());

        return self.__rc;

    def setConfig(self, config):
        assert isinstance(config, ConfigStructure);

        self.__rc = config;

    def getPath(self):
        if None is not self.__path :
            return self.__path;

        path = None;

        # Take most of our configuration from .cyg-apt
        # preferring .cyg-apt in current directory over $(HOME)/.cyg-apt
        cwd_cyg_apt_rc = os.path.join(
            os.getcwd(),
            ".{0}".format(self.__platform.getAppName())
        );
        if os.path.exists(cwd_cyg_apt_rc):
            path = cwd_cyg_apt_rc;
        elif "HOME" in os.environ:
            home_cyg_apt_rc = os.path.join(
                os.environ['HOME'],
                ".{0}".format(self.__platform.getAppName())
            );
            if os.path.exists(home_cyg_apt_rc):
                path = home_cyg_apt_rc;

        self.__path = path;

        return path;

    def __parse(self, path):
        """Currently main only needs to know if we alway call the update command
        before other commands
        """
        f = open(path);
        lines = f.readlines();
        f.close();

        rc_regex = re.compile(r"^\s*(\w+)\s*=\s*(.*)\s*$");
        always_update = False;
        for i in lines:
            result = rc_regex.search(i);
            if result:
                k = result.group(1);
                v = result.group(2);
                if k == "always_update":
                    always_update = eval(v);
                if k in self.__rc.__dict__:
                    self.__rc.__dict__[k] = eval(v);

        if always_update in [True, 'True', 'true', 'Yes', 'yes']:
            always_update = True;
        else:
            always_update = False;

        self.__rc.__dict__['always_update'] = always_update;

        self.__parsed = True;
