# -*- coding: utf-8 -*-
# This file is part of the pymfony package.
#
# (c) Alexandre Quercia <alquerci@email.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from os.path import dirname;

from pymfony.component.kernel import Kernel;
from pymfony.component.config.loader import LoaderInterface;
from pymfony.bundle.framework_bundle import FrameworkBundle;

from cygapt.cygapt_bundle import CygAptBundle;

"""
"""

class AppKernel(Kernel):
    VERSION = '2.0.0-DEV';
    VERSION_ID = '20000';
    MAJOR_VERSION = '2';
    MINOR_VERSION = '0';
    RELEASE_VERSION = '0';
    EXTRA_VERSION = 'DEV';

    def registerBundles(self):
        bundles = [
            FrameworkBundle(),
            CygAptBundle(),
        ];

        return bundles;


    def registerContainerConfiguration(self, loader):
        assert isinstance(loader, LoaderInterface);

        loader.load("{0}/Resources/config/config_{1}.yml".format(
            dirname(__file__),
            self.getEnvironment()
        ));

    def getName(self):
        return 'cyg-apt';
