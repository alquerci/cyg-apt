# -*- coding: utf-8 -*-
# This file is part of the cygapt package.
#
# (c) Alexandre Quercia <alquerci@email.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.

from __future__ import absolute_import;

from pymfony.component.dependency import ContainerAware;
from pymfony.component.console import Response;
from pymfony.bundle.framework_bundle.command import ExceptionCommand as BaseExceptionCommand;
from pymfony.component.console import Request;
from pymfony.component.console_routing import Router;

from cygapt.setup import CygAptSetup;
from cygapt.exception import ApplicationException;
from cygapt.cygapt import CygApt

"""
"""

class ExceptionCommand(BaseExceptionCommand):
    def showAction(self, request, exception):
        if isinstance(exception, ApplicationException):
            return Response('<error>'+str(exception)+'</error>');

        return BaseExceptionCommand.showAction(self, request, exception);

class SetupCommand(ContainerAware):
    def updateAction(self, _o_verbose, _o_no_verify, _o_mirror):
        isCygwin = self._container.getParameter('cyg_apt.cygwin');
        resource = self._container.getParameter('cyg_apt.resource');

        ob = self._container.get('cyg_apt.ob');
        ob.start();

        try:
            cas = CygAptSetup(isCygwin, _o_verbose);

            cas.update(resource, not _o_no_verify, _o_mirror);

            content = ob.getContents();
        finally:
            ob.endClean();

        return Response(content);

    def setupAction(self, _o_verbose, _o_force):
        isCygwin = self._container.getParameter('cyg_apt.cygwin');

        ob = self._container.get('cyg_apt.ob');
        ob.start();

        try:
            cas = CygAptSetup(isCygwin, _o_verbose);
            cas.setAppName(self._container.getParameter('kernel.name'));
            cas.setup(_o_force);

            content = ob.getContents();
        finally:
            ob.endClean();

        return Response(content);


class CygAptCommand(ContainerAware):
    def ballAction(self, request, package):
        ob = self._container.get('cyg_apt.ob');
        ob.start();

        try:
            self._getCygApt(request, [package]).ball();
            content = ob.getContents();
        finally:
            ob.endClean();

        if not content:
            content = '';

        return Response(content);

    def downloadAction(self, request, package):
        ob = self._container.get('cyg_apt.ob');
        ob.start();

        try:
            self._getCygApt(request, [package]).download();
            content = ob.getContents();
        finally:
            ob.endClean();

        if not content:
            content = '';

        return Response(content);

    def filelistAction(self, request, package):
        ob = self._container.get('cyg_apt.ob');
        ob.start();

        try:
            self._getCygApt(request, [package]).filelist();
            content = ob.getContents();
        finally:
            ob.endClean();

        if not content:
            content = '';

        return Response(content);

    def findAction(self, request, filename):
        ob = self._container.get('cyg_apt.ob');
        ob.start();

        try:
            self._getCygApt(request, [filename]).find();
            content = ob.getContents();
        finally:
            ob.endClean();

        if not content:
            content = '';

        return Response(content);

    def installAction(self, request, packages):
        ob = self._container.get('cyg_apt.ob');
        ob.start();

        try:
            self._getCygApt(request, packages).install();
            content = ob.getContents();
        finally:
            ob.endClean();

        if not content:
            content = '';

        return Response(content);

    def listAction(self, request):
        ob = self._container.get('cyg_apt.ob');
        ob.start();

        try:
            self._getCygApt(request).list();
            content = ob.getContents();
        finally:
            ob.endClean();

        if not content:
            content = '';

        return Response(content);

    def md5Action(self, request, package):
        ob = self._container.get('cyg_apt.ob');
        ob.start();

        try:
            self._getCygApt(request, [package]).md5();
            content = ob.getContents();
        finally:
            ob.endClean();

        if not content:
            content = '';

        return Response(content);

    def missingAction(self, request, package):
        ob = self._container.get('cyg_apt.ob');
        ob.start();

        try:
            self._getCygApt(request, [package]).missing();
            content = ob.getContents();
        finally:
            ob.endClean();

        if not content:
            content = '';

        return Response(content);

    def newAction(self, request):
        ob = self._container.get('cyg_apt.ob');
        ob.start();

        try:
            self._getCygApt(request).new();
            content = ob.getContents();
        finally:
            ob.endClean();

        if not content:
            content = '';

        return Response(content);

    def purgeAction(self, request, packages):
        ob = self._container.get('cyg_apt.ob');
        ob.start();

        try:
            self._getCygApt(request, packages).purge();
            content = ob.getContents();
        finally:
            ob.endClean();

        if not content:
            content = '';

        return Response(content);

    def removeAction(self, request, packages):
        ob = self._container.get('cyg_apt.ob');
        ob.start();

        try:
            self._getCygApt(request, packages).remove();
            content = ob.getContents();
        finally:
            ob.endClean();

        if not content:
            content = '';

        return Response(content);

    def requiresAction(self, request, package):
        ob = self._container.get('cyg_apt.ob');
        ob.start();

        try:
            self._getCygApt(request, [package]).requires();
            content = ob.getContents();
        finally:
            ob.endClean();

        if not content:
            content = '';

        return Response(content);

    def searchAction(self, request, string):
        ob = self._container.get('cyg_apt.ob');
        ob.start();

        try:
            self._getCygApt(request, [string]).search();
            content = ob.getContents();
        finally:
            ob.endClean();

        if not content:
            content = '';

        return Response(content);

    def showAction(self, request, package):
        ob = self._container.get('cyg_apt.ob');
        ob.start();

        try:
            self._getCygApt(request, [package]).show();
            content = ob.getContents();
        finally:
            ob.endClean();

        if not content:
            content = '';

        return Response(content);

    def sourceAction(self, request, packages):
        ob = self._container.get('cyg_apt.ob');
        ob.start();

        try:
            self._getCygApt(request, packages).source();
            content = ob.getContents();
        finally:
            ob.endClean();

        if not content:
            content = '';

        return Response(content);

    def upgradeAction(self, request):
        ob = self._container.get('cyg_apt.ob');
        ob.start();

        try:
            self._getCygApt(request).upgrade();
            content = ob.getContents();
        finally:
            ob.endClean();

        if not content:
            content = '';

        return Response(content);

    def urlAction(self, request, package):
        ob = self._container.get('cyg_apt.ob');
        ob.start();

        try:
            self._getCygApt(request, [package]).url();
            content = ob.getContents();
        finally:
            ob.endClean();

        if not content:
            content = '';

        return Response(content);

    def versionAction(self, request, packages):
        ob = self._container.get('cyg_apt.ob');
        ob.start();

        try:
            self._getCygApt(request, packages).version();
            content = ob.getContents();
        finally:
            ob.endClean();

        if not content:
            content = '';

        return Response(content);

    def _getCygApt(self, request, packages = None):
        if packages is None:
            packages = list();
        assert isinstance(request, Request);
        assert isinstance(packages, list);

        isCygwin = self._container.getParameter('cyg_apt.cygwin');
        appName = self._container.getParameter('kernel.name');
        resource = self._container.getParameter('cyg_apt.resource');
        downloads = None;
        dists = 0;
        installed = 0;
        packageName = None;

        files = packages[:];
        files.insert(0, request.getArgument(Router.COMMAND_KEY));
        if packages:
            packageName = packages[0];

        cygApt = CygApt(
            packageName,
            files,
            resource,
            isCygwin,
            request.getOption('download'),
            request.getOption('mirror'),
            downloads,
            request.getOption('dist'),
            request.getOption('no-deps'),
            request.getOption('regexp'),
            request.getOption('nobarred'),
            request.getOption('nopostinstall'),
            request.getOption('nopostremove'),
            dists,
            installed,
            appName,
            request.getOption('verbose')
        );

        return cygApt;
