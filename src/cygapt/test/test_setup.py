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
"""
    Unit test for cygapt.setup
"""

from __future__ import absolute_import;

import unittest;
import sys;
import os;
import subprocess;

from cygapt.setup import CygAptSetup;
from cygapt.test.utils import TestCase;
from cygapt.test.utils import SetupIniProvider;
from cygapt.setup import PlatformException;
from cygapt.setup import EnvironementException;
from cygapt.exception import PathExistsException;
from cygapt.exception import UnexpectedValueException;
from cygapt.setup import SignatureException;
from cygapt.ob import CygAptOb;
from cygapt.configuration import Configuration;
from cygapt.platform import Platform;
from cygapt.input import Input;
from cygapt.path_mapper import PathMapper;


class TestSetup(TestCase):
    def setUp(self):
        TestCase.setUp(self);
        self._var_verbose = False;
        self._var_cygwin_p = sys.platform.startswith("cygwin");
        self._var_verify = True;

        self._inputMock = self._createInputMock();
        self.obj = self._createSetup();

    def test__init__(self):
        self.assertTrue(isinstance(self.obj, CygAptSetup));
        self.assertEqual(self.obj.getCygwinPlatform(), self._var_cygwin_p);

    def testGetSetupRc(self):
        if not self._var_cygwin_p:
            self.skipTest("requires cygwin");

        badlocation = os.path.join(self._var_tmpdir, "not_exist_file");
        last_cache, last_mirror = self.obj.getSetupRc(badlocation);
        self.assertEqual(last_cache, None);
        self.assertEqual(last_mirror, None);

        last_cache, last_mirror = self.obj.getSetupRc(self._dir_confsetup);
        self.assertEqual(last_cache, self._dir_execache);
        self.assertEqual(last_mirror, self._var_mirror);

    def testGetPre17Last(self):
        if not self._var_cygwin_p:
            self.skipTest("requires cygwin");

        location = self._var_tmpdir;
        last_mirror = "http://cygwin.uib.no/";
        last_cache = os.path.join(self._var_tmpdir, "last_cache");
        os.mkdir(last_cache);
        lm_file = os.path.join(self._var_tmpdir, "last-mirror");
        lc_file = os.path.join(self._var_tmpdir, "last-cache");
        lm_stream = open(lm_file, 'w');
        lm_stream.write(last_mirror);
        lm_stream.close();
        lc_stream = open(lc_file, 'w');
        lc_stream.write(last_cache);
        lc_stream.close();

        rlast_cache, rlast_mirror = self.obj._getPre17Last(location);
        self.assertEqual(last_cache, rlast_cache);
        self.assertEqual(last_mirror, rlast_mirror);

    def testUpdateWithGoodMirrorSignature(self):
        if not self._var_cygwin_p:
            self.skipTest("requires cygwin");

        self._writeUserConfig(self._file_user_config);
        self._var_mirror = self._var_mirror_http;

        self.obj._gpgImport(self.obj.GPG_CYG_PUBLIC_RING_URI);
        self.obj.update(self._createInputMock());

    def testUpdateWithBadMirrorSignature(self):
        if not self._var_cygwin_p:
            self.skipTest("requires cygwin");

        self._writeUserConfig(self._file_user_config);
        self.obj._gpgImport(self.obj.GPG_CYG_PUBLIC_RING_URI);

        try:
            self.obj.update(self._inputMock);
        except Exception as e:
            self.assertTrue(isinstance(e, SignatureException));
            self.assertEqual(e.getMessage(), " ".join([
                "{0}/{1}/setup.bz2 not signed by Cygwin's public key.",
                "Use -X to ignore signatures.",
            ]).format(self._var_mirror, self._var_setupIni.getArchitecture()));
        else:
            self.fail(" ".join([
                ".update() raises an SignatureException when the mirror have",
                "not the Cygwin signature.",
            ]));

    def testUpdateWithoutVerifySignature(self):
        if not self._var_cygwin_p:
            self.skipTest("requires cygwin");

        self._writeUserConfig(self._file_user_config);
        self._var_verify = False;

        inputMock = self._createInputMock();
        self.obj.update(inputMock);

        self._assertUpdate();

    def testUpdateWithoutVerifySignatureOn64Bit(self):
        if not self._var_cygwin_p:
            self.skipTest("requires cygwin");

        self._var_arch = "x86_64";
        self._var_setupIni = SetupIniProvider(self, self._var_arch);
        self.obj.setArchitecture(self._var_arch);

        self._writeUserConfig(self._file_user_config);
        self._var_verify = False;

        inputMock = self._createInputMock();
        self.obj.update(inputMock);

        self._assertUpdate();

    def testUpdateWithoutMirror(self):
        if not self._var_cygwin_p:
            self.skipTest("requires cygwin");

        self._var_mirror = "";
        self._writeUserConfig(self._file_user_config);
        self._var_verify = False;

        inputMock = self._createInputMock();
        self.obj = self._createSetup();

        try:
            self.obj.update(inputMock);
        except Exception as e:
            self.assertTrue(isinstance(e, UnexpectedValueException));
            self.assertEqual(e.getMessage(), (
                "A mirror must be specified on the configuration file \"{0}\" "
                "or with the command line option \"--mirror\". "
                "See cygwin.com/mirrors.html for the list of mirrors."
                "".format(self._file_user_config)
            ));
        else:
            self.fail(
                ".update() raises an UnexpectedValueException if the mirror "
                "was not defined."
            );

    def testSetup(self):
        if not self._var_cygwin_p:
            self.assertRaises(PlatformException, self.obj.setup);
            return;

        # env HOME not exists
        os.environ.pop('HOME');
        self.assertRaises(EnvironementException, self.obj.setup, self._inputMock);
        os.environ['HOME'] = self._dir_user;

        # config file already isset
        f = open(self._file_user_config, 'w');
        f.close();
        self.assertRaises(PathExistsException, self.obj.setup, self._inputMock);
        self.assertTrue(os.path.exists(self._file_user_config));

        os.remove(self._file_user_config);

        # next
        self._var_mirror = self._var_mirror_http;
        self._writeSetupRc(self._file_setup_rc);

        inputMock = self._createInputMock();
        self.obj._gpgImport(self.obj.GPG_CYG_PUBLIC_RING_URI);
        self.obj.setup(inputMock);

    def testWriteInstalled(self):
        if not self._var_cygwin_p:
            self.skipTest("requires cygwin");

        real_installed_db = self._file_installed_db.replace(self._var_tmpdir, "");
        self.obj._writeInstalled(self._file_installed_db);
        self.assertTrue(os.path.exists(self._file_installed_db));
        f = open(self._file_installed_db);
        ret = f.readlines().sort();
        f.close();
        f = open(real_installed_db);
        expected = f.readlines().sort();
        f.close();
        self.assertEqual(ret, expected);

    def testGpgImport(self):
        if not self._var_cygwin_p:
            self.skipTest("requires cygwin");

        self.obj._gpgImport(self.obj.GPG_CYG_PUBLIC_RING_URI);

        cmd = " ".join([
            "gpg",
            "--no-secmem-warning",
            "--list-public-keys",
            "--fingerprint",
        ]);
        p = subprocess.Popen(cmd, shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE);
        if p.wait():
            raise RuntimeError(p.stderr.read());
        lines = p.stdout.readlines();
        findout = False;
        for line in lines:
            if isinstance(line, bytes):
                marker = self.obj.GPG_GOOD_FINGER.encode();
            else:
                marker = self.obj.GPG_GOOD_FINGER;
            if marker in line:
                findout = True;
                break;

        self.assertTrue(findout);

    def testUsage(self):
        self.obj.usage(self._inputMock);

    def testUsageContainPostInstallCommand(self):
        self._assertUsageContainCommand("postinstall");

    def testUsageContainPostRemoveCommand(self):
        self._assertUsageContainCommand("postremove");

    def _assertUsageContainCommand(self, command):
        ob = CygAptOb(True);
        self.obj.usage(self._inputMock);
        ret = ob.getClean();

        self.assertTrue("    {0}".format(command) in ret);

    def _assertUpdate(self):
        """Asserts that the local setup.ini has been updated.

        @raise AssertionError: When the assertion is not verify.
        """
        onCache = os.path.join(
            self._dir_downloads,
            self._var_setupIni.getArchitecture(),
            "setup.ini"
        );
        onEtc = self._file_setup_ini;

        self.assertTrue(os.path.isfile(onCache), onCache+" not exists.");
        self.assertTrue(os.path.isfile(onEtc), onEtc+" not exists.");

        expected = self._var_setupIni.contents;

        with open(onCache, 'r') as f :
            actual = f.read();
        self.assertEqual(expected, actual);

        with open(onEtc, 'r') as f :
            actual = f.read();
        self.assertEqual(expected, actual);

    def _createInputMock(self):
        inputMock = self.getMock(Input);
        inputMock.getOption.expects(self.atLeastOnce())\
            .will(self.returnValueMap([
                ('verbose', {}, self._var_verbose),
                ('mirror',  {}, self._var_mirror),
                ('force',   {}, False),
                ('verify',  {}, self._var_verify),
            ]))\
        ;

        return inputMock;

    def _createSetup(self):
        platformMock = self.getMock(Platform);
        platformMock.isCygwin.expects(self.once())\
            .will(self.returnValue(self._var_cygwin_p))\
        ;
        platformMock.getAppName.expects(self.once())\
            .will(self.returnValue(self._var_exename))\
        ;
        platformMock.getArchitecture.expects(self.any())\
            .will(self.returnValue(self._var_arch))\
        ;

        configMock = self.getMock(Configuration);
        configMock.getPath.expects(self.once())\
            .will(self.returnValue(self._file_user_config))\
        ;
        configMock.get.expects(self.atLeastOnce())\
            .will(self.returnValueMap([
                ('ROOT',            {}, self._dir_mtroot),
                ('mirror',          {}, self._var_mirror),
                ('cache',           {}, self._dir_execache),
                ('setup_ini',       {}, self._file_setup_ini),
                ('distname',        {}, 'curr'),
                ('barred',          {}, ''),
                ('always_update',   {}, False),
            ]))\
        ;

        pathMapperMock = self.getMock(PathMapper);
        def pathCallback(path):
            if path.startswith(self._dir_mtroot) :
                return path;
            return self._dir_mtroot[:-1]+path;
        pathMapperMock.mapPath.expects(self.atLeastOnce())\
            .will(self.returnCallback(pathCallback))\
        ;
        pathMapperMock.getMountRoot.expects(self.atLeastOnce())\
            .will(self.returnValue(self._dir_mtroot))\
        ;

        setup = CygAptSetup(configMock, platformMock, pathMapperMock);
        setup.setTmpDir(self._dir_tmp);
        setup.setSetupDir(self._dir_confsetup);

        return setup;

if __name__ == "__main__":
    unittest.main()
