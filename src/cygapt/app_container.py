# -*- coding: utf-8 -*-
# This file is part of the cygapt package.
#
# (c) Alexandre Quercia <alquerci@email.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.

from __future__ import absolute_import;

from cygapt.container import Container;
from cygapt.application import Application;
from cygapt.argparser import CygAptArgParser;
from cygapt.path_mapper import PathMapper;
from cygapt.setup import CygAptSetup;
from cygapt.cygapt import CygApt;
from cygapt.ob import CygAptOb;
from cygapt.platform import Platform;
from cygapt.configuration import Configuration;

"""
"""

class AppContainer(Container):
    def __init__(self):
        Container.__init__(self);

        self._parameters = self.getDefaultParameters();

        self.set("service_container", self);

    def getApplicationService(self):
        self._services['application'] = instance = Application(self, self.get('configuration'), self.get('platform'));

        return instance;

    def getOutputBufferService(self):
        self._services['output_buffer'] = instance = CygAptOb();

        return instance;

    def getArgParserService(self):
        ob = self.get('output_buffer');
        ob.start();
        self.get('setup').usage();
        usage = ob.getFlush();

        self._services['arg_parser'] = instance = CygAptArgParser(usage, self.get('platform').getAppName());

        return instance;

    def getPlatformService(self):
        self._services['platform'] = instance = Platform();

        return instance;

    def getPathMapperService(self):
        self._services['path_mapper'] = instance = PathMapper(self.get('configuration'), self.get('platform'));

        return instance;

    def getConfigurationService(self):
        self._services['configuration'] = instance = Configuration(self.get('platform'));

        return instance;

    def getSetupService(self):
        self._services['setup'] = instance = CygAptSetup(self.get('configuration'), self.get('platform'), self.get('path_mapper'));

        return instance;

    def getCommand_SetupService(self):
        self._services['command.setup'] = instance = _NullCommand();

        instance.run = self.get('setup').setup;

        return instance;

    def getCommand_UpdateService(self):
        self._services['command.update'] = instance = _NullCommand();

        instance.run = self.get('setup').update;

        return instance;

    def getCommand_HelpService(self):
        self._services['command.help'] = instance = _NullCommand();

        instance.run = self.get('setup').usage;

        return instance;

    def getCygaptService(self):
        self._services['cygapt'] = instance = CygApt(self.get('configuration'), self.get('platform'), self.get('path_mapper'));

        return instance;

    def getCommand_UrlService(self):
        self._services['command.url'] = instance = _NullCommand();

        instance.run = self.get('cygapt').url;

        return instance;

    def getCommand_BallService(self):
        self._services['command.ball'] = instance = _NullCommand();

        instance.run = self.get('cygapt').ball;

        return instance;

    def getCommand_DownloadService(self):
        self._services['command.download'] = instance = _NullCommand();

        instance.run = self.get('cygapt').download;

        return instance;

    def getCommand_RequiresService(self):
        self._services['command.requires'] = instance = _NullCommand();

        instance.run = self.get('cygapt').requires;

        return instance;

    def getCommand_ListService(self):
        self._services['command.list'] = instance = _NullCommand();

        instance.run = self.get('cygapt').list;

        return instance;

    def getCommand_FilelistService(self):
        self._services['command.filelist'] = instance = _NullCommand();

        instance.run = self.get('cygapt').filelist;

        return instance;

    def getCommand_VersionService(self):
        self._services['command.version'] = instance = _NullCommand();

        instance.run = self.get('cygapt').version;

        return instance;

    def getCommand_NewService(self):
        self._services['command.new'] = instance = _NullCommand();

        instance.run = self.get('cygapt').new;

        return instance;

    def getCommand_Md5Service(self):
        self._services['command.md5'] = instance = _NullCommand();

        instance.run = self.get('cygapt').md5;

        return instance;

    def getCommand_ShowService(self):
        self._services['command.show'] = instance = _NullCommand();

        instance.run = self.get('cygapt').show;

        return instance;

    def getCommand_MissingService(self):
        self._services['command.missing'] = instance = _NullCommand();

        instance.run = self.get('cygapt').missing;

        return instance;

    def getCommand_RemoveService(self):
        self._services['command.remove'] = instance = _NullCommand();

        instance.run = self.get('cygapt').remove;

        return instance;

    def getCommand_PurgeService(self):
        self._services['command.purge'] = instance = _NullCommand();

        instance.run = self.get('cygapt').purge;

        return instance;

    def getCommand_InstallService(self):
        self._services['command.install'] = instance = _NullCommand();

        instance.run = self.get('cygapt').install;

        return instance;

    def getCommand_PostinstallService(self):
        self._services['command.postinstall'] = instance = _NullCommand();

        instance.run = self.get('cygapt').postinstall;

        return instance;

    def getCommand_PostremoveService(self):
        self._services['command.postremove'] = instance = _NullCommand();

        instance.run = self.get('cygapt').postremove;

        return instance;

    def getCommand_UpgradeService(self):
        self._services['command.upgrade'] = instance = _NullCommand();

        instance.run = self.get('cygapt').upgrade;

        return instance;

    def getCommand_SourceService(self):
        self._services['command.source'] = instance = _NullCommand();

        instance.run = self.get('cygapt').source;

        return instance;

    def getCommand_FindService(self):
        self._services['command.find'] = instance = _NullCommand();

        instance.run = self.get('cygapt').find;

        return instance;

    def getDefaultParameters(self):
        return {
        };

class _NullCommand():
    def run(self):
        pass;

