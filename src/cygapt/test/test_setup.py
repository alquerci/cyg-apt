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
import urllib;

from cygapt.setup import CygAptSetup;
from cygapt.test.utils import TestCase;
from cygapt.test.utils import SetupIniProvider;
from cygapt.setup import PlatformException;
from cygapt.setup import EnvironementException;
from cygapt.exception import PathExistsException;
from cygapt.exception import UnexpectedValueException;
from cygapt.setup import SignatureException;
from cygapt.ob import CygAptOb;
from cygapt.config import GPG;


class TestSetup(TestCase):
    def setUp(self):
        TestCase.setUp(self);
        self._var_verbose = False;
        self._var_cygwin_p = (
            sys.platform.startswith("cygwin")
            or sys.platform.startswith("linux")
        );
        self.obj = CygAptSetup(
            self._var_cygwin_p,
            self._var_verbose,
            self._var_arch,
        );
        self.obj.setTmpDir(self._dir_tmp);
        self.obj.setAppName(self._var_exename);
        self.obj.setSetupDir(self._dir_confsetup);
        self.obj.getRC().ROOT = self._dir_mtroot;

    def test__init__(self):
        self.assertTrue(isinstance(self.obj, CygAptSetup));
        self.assertEqual(self.obj.getCygwinPlatform(), self._var_cygwin_p);
        self.assertEqual(self.obj.getVerbose(), self._var_verbose);

    def testGetSetupRc(self):
        badlocation = os.path.join(self._var_tmpdir, "not_exist_file");
        last_cache, last_mirror = self.obj.getSetupRc(badlocation);
        self.assertEqual(last_cache, None);
        self.assertEqual(last_mirror, None);

        last_cache, last_mirror = self.obj.getSetupRc(self._dir_confsetup);
        self.assertEqual(last_cache, self._dir_execache);
        self.assertEqual(last_mirror, self._var_mirror);

    def testGetPre17Last(self):
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
            self.skipTest("requires cygwin or linux");

        self._writeUserConfig(self._file_user_config);

        self.obj._gpgImport(self.obj.GPG_CYG_PUBLIC_RING_URI);
        self.obj.update(self._file_user_config, True, self._var_mirror_http);

    def testUpdateWithBadMirrorSignature(self):
        if not self._var_cygwin_p:
            self.skipTest("requires cygwin or linux");

        self._writeUserConfig(self._file_user_config);
        self.obj._gpgImport(self.obj.GPG_CYG_PUBLIC_RING_URI);

        try:
            self.obj.update(self._file_user_config, True);
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
            self.skipTest("requires cygwin or linux");

        self._writeUserConfig(self._file_user_config);

        self.obj.update(self._file_user_config, False);

        self._assertUpdate();

    def testUpdateWithoutVerifySignatureOn64Bit(self):
        if not self._var_cygwin_p:
            self.skipTest("requires cygwin or linux");

        self._var_arch = "x86_64";
        self._var_setupIni = SetupIniProvider(self, self._var_arch);
        self.obj.setArchitecture(self._var_arch);

        self._writeUserConfig(self._file_user_config);

        self.obj.update(self._file_user_config, False);

        self._assertUpdate();

    def testUpdateWithoutMirror(self):
        if not self._var_cygwin_p:
            self.skipTest("requires cygwin or linux");

        self._var_mirror = "";
        self._writeUserConfig(self._file_user_config);

        try:
            self.obj.update(self._file_user_config, False);
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

    def testUpdateWithSetupIniFieldWarnDeprecationWarning(self):
        if not self._var_cygwin_p:
            self.skipTest("requires cygwin");

        self._writeUserConfig(self._file_user_config, keepBC=True);

        self._assertDeprecatedWarning(
            "The configuration field `setup_ini` is deprecated since version"
            " 1.1 and will be removed in 2.0.",
            self.obj.update,
            self._file_user_config,
            False,
        );

        self._assertUpdate(keepBC=True);

    def testUpdateWithoutSetupIniFieldNotWarnDeprecationWarning(self):
        if not self._var_cygwin_p:
            self.skipTest("requires cygwin");

        self._writeUserConfig(self._file_user_config);

        self._assertNotDeprecatedWarning(
            "The configuration field `setup_ini` is deprecated since version"
            " 1.1 and will be removed in 2.0.",
            self.obj.update,
            self._file_user_config,
            False,
        );

    def testSetup(self):
        if not self._var_cygwin_p:
            self.assertRaises(PlatformException, self.obj.setup);
            return;

        # env HOME not exists
        os.environ.pop('HOME');
        self.assertRaises(EnvironementException, self.obj.setup);
        os.environ['HOME'] = self._dir_user;

        # config file already isset
        f = open(self._file_user_config, 'w');
        f.close();
        self.assertRaises(PathExistsException, self.obj.setup);
        self.assertTrue(os.path.exists(self._file_user_config));

        os.remove(self._file_user_config);

        # next
        self._var_mirror = self._var_mirror_http;
        self._writeSetupRc(self._file_setup_rc);
        self.obj._gpgImport(self.obj.GPG_CYG_PUBLIC_RING_URI);
        self.obj.setup();

        # create a default user configuration file
        self.assertTrue(os.path.isfile(self._file_user_config));
        with open(self._file_user_config, 'r') as f :
            self.assertEqual("\n".join([
                "# The distribution, current previous or test [curr, prev, test].",
                '# Usually you want the "curr" version of a package.',
                'distname="curr"',
                "",
                "# Your package cache as a POSIX path: example /e/home/cygwin_package_cache",
                'cache="{self[_dir_execache]}"',
                "",
                "# Packages which cyg-apt can't change under Cygwin since it depends on them.",
                "# Run cyg-apt under DOS with -f (force) option to change these packages.",
                "# Treat Cygwin core packages with CAUTION.",
                'barred=""',
                "",
                "# URL of your Cygwin mirror: example http://mirror.internode.on.net/pub/cygwin/",
                'mirror="{self[_var_mirror]}"',
                "",
                "# Always update setup.ini before any command that uses it. cyg-apt will be",
                "# faster and use less bandwidth if False but you will have to run the update",
                "# command manually.",
                'always_update="False"',
                "",
                "# setup.ini lists available packages and is downloaded from the top level",
                "# of the downloaded mirror. Standard location is /etc/setup/setup.ini,",
                "# seutp-2.ini for Cygwin 1.7 Beta",
                "# Deprecated since version 1.1 and will be removed in 2.0.",
                '# setup_ini="{self[_file_setup_ini]}"',
                "",
                "# The root of your Cygwin installation as a windows path",
                'ROOT="{self[_dir_mtroot]}"',
                "",
                "",
            ]).format(self=vars(self)), f.read());

        # create setup.ini on `/etc/setup/`
        self.assertFalse(os.path.isfile(self._file_setup_ini));

        # create setup.ini on `<cachedir>/<mirror>/<arch>/`
        self.assertTrue(os.path.isfile(os.path.join(
            self._dir_execache,
            urllib.quote(self._var_mirror, '').lower(),
            self._var_arch,
            "setup.ini",
        )));

    def testSetupNotWarnDeprecationWarning(self):
        if not self._var_cygwin_p:
            self.skipTest("requires cygwin");

        self._var_mirror = self._var_mirror_http;
        self._writeSetupRc(self._file_setup_rc);
        self.obj._gpgImport(self.obj.GPG_CYG_PUBLIC_RING_URI);

        self._assertNotDeprecatedWarning(
            "The configuration field `setup_ini` is deprecated since version"
            " 1.1 and will be removed in 2.0.",
            self.obj.setup,
        );

    def testWriteInstalled(self):
        if not sys.platform.startswith("cygwin"):
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
            self.skipTest("requires cygwin or linux");

        self.obj._gpgImport(self.obj.GPG_CYG_PUBLIC_RING_URI);

        cmd = " ".join([
            GPG,
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
        self.obj.usage();

    def testUsageContainPostInstallCommand(self):
        self._assertUsageContainCommand("postinstall");

    def testUsageContainPostRemoveCommand(self):
        self._assertUsageContainCommand("postremove");

    def _assertUsageContainCommand(self, command):
        ob = CygAptOb(True);
        self.obj.usage();
        ret = ob.getClean();

        self.assertTrue("    {0}".format(command) in ret);

    def _assertUpdate(self, keepBC=False):
        """Asserts that the local setup.ini has been updated.

        @raise AssertionError: When the assertion is not verify.
        """
        onCache = os.path.join(
            self._dir_downloads,
            self._var_setupIni.getArchitecture(),
            "setup.ini"
        );

        self.assertTrue(os.path.isfile(onCache), onCache+" not exists.");

        expected = self._var_setupIni.contents;

        with open(onCache, 'r') as f :
            actual = f.read();
        self.assertEqual(expected, actual);

        if not keepBC :
            return;

        # BC layer for `setup_ini` configuration field
        onEtc = self._file_setup_ini;
        self.assertTrue(os.path.isfile(onEtc), onEtc+" not exists.");
        with open(onEtc, 'r') as f :
            actual = f.read();
        self.assertEqual(expected, actual);

if __name__ == "__main__":
    unittest.main()
