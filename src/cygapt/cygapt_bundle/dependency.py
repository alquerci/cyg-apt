# -*- coding: utf-8 -*-
# This file is part of the cygapt package.
#
# (c) Alexandre Quercia <alquerci@email.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from os.path import dirname;
import sys;
import os;

from pymfony.component.kernel.dependency import Extension;
from pymfony.component.dependency.loader import YamlFileLoader;
from pymfony.component.config import FileLocator;
from cygapt.exception import ApplicationException

"""
"""

class CygAptExtension(Extension):
    def load(self, configs, container):
        loader = YamlFileLoader(container, FileLocator(dirname(__file__)+'/Resources/config'))
        loader.load("services.yml");

        container.setParameter('cyg_apt.cygwin', sys.platform.startswith("cygwin"));

        container.setParameter('cyg_apt.resource', self.__resolveMainCygAptResource('cyg-apt'));

    def getAlias(self):
        return 'cyg_apt';

    def __resolveMainCygAptResource(self, name):
        # Take most of our configuration from .cyg-apt
        # preferring .cyg-apt in current directory over $(HOME)/.cyg-apt
        cwd_cyg_apt_rc = os.path.join(os.getcwd(), ".{0}".format(name));

        main_cyg_apt_rc = '';

        if os.path.exists(cwd_cyg_apt_rc):
            main_cyg_apt_rc = cwd_cyg_apt_rc;
        elif "HOME" in os.environ:
            home_cyg_apt_rc = os.path.join(os.environ['HOME'], ".{0}".format(name));

            if os.path.exists(home_cyg_apt_rc):
                main_cyg_apt_rc = home_cyg_apt_rc;

        if main_cyg_apt_rc:
            # Take our configuration from .cyg-apt
            # Command line options can override, but only for this run.
            main_cyg_apt_rc = main_cyg_apt_rc.replace("\\","/");
        else:
            raise ApplicationException("{0}: no .{0}: run \"{0} setup\"".format(name));

        return main_cyg_apt_rc;
