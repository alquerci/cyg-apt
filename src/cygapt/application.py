# -*- coding: utf-8 -*-
# This file is part of the cygapt package.
#
# (c) Alexandre Quercia <alquerci@email.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.

from __future__ import absolute_import;
from __future__ import print_function;

import sys;

from cygapt.container import Container;
from cygapt.input import Input;
from cygapt.configuration import Configuration;
from cygapt.exception import InvalidArgumentException;
from cygapt.platform import Platform;

"""
"""

class Application():
    __updateNotNeeded = [
        "ball",
        "find",
        "help",
        "purge",
        "remove",
        "version",
        "filelist",
        "update",
        "setup",
        "md5",
    ];

    def __init__(self, container, configuration, platform):
        assert isinstance(container, Container);
        assert isinstance(configuration, Configuration);
        assert isinstance(platform, Platform);

        self._container = container;
        self._config = configuration;
        self._platform = platform;

    def run(self, input_):
        assert isinstance(input_, Input);

        commandName = input_.getArgument('command');

        if None is self._config.getPath() and commandName != "setup" :
            print(
                "{0}: no .{0}: run \"{0} setup\"".format(self._platform.getAppName()),
                file=sys.stderr
            );

            return 1;

        try:
            command = self._container.get("command."+commandName);
        except InvalidArgumentException :
            command = self._container.get("command.help");
            commandName = 'help';

        if (self._config.get('always_update')
            and commandName not in self.__updateNotNeeded
            and not input_.getOption('noupdate')
        ) :
            self._container.get("command.update").run(input_);

        command.run(input_);

        return 0;
