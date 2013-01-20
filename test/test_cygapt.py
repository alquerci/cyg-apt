#!/usr/bin/python
######################## BEGIN LICENSE BLOCK ########################
# This file is part of the cygapt package.
#
# Copyright (C) 2002-2009 Jan Nieuwenhuizen  <janneke@gnu.org>
#               2002-2009 Chris Cormie       <cjcormie@gmail.com>
#                    2012 James Nylen        <jnylen@gmail.com>
#               2012-2013 Alexandre Quercia  <alquerci@email.com>
#
# For the full copyright and license information, please view the
# LICENSE file that was distributed with this source code.
######################### END LICENSE BLOCK #########################

from __future__ import print_function;
import unittest;
import sys;
import os;
import gzip;

from cygapt.cygapt import CygApt;
from cygapt.setup import CygAptSetup;
from cygapt.ob import CygAptOb;
import cygapt.utilstest;

class TestCygApt(cygapt.utilstest.TestCase):
    def setUp(self):
        cygapt.utilstest.TestCase.setUp(self);

        self._var_verbose = False;
        self._var_cygwin_p = sys.platform == "cygwin";

        if not self._var_cygwin_p:
            self.skipTest("requires cygwin");

        setup = CygAptSetup(self._var_cygwin_p, self._var_verbose);
        setup.tmpdir = self._dir_tmp;
        setup.appName = self._var_exename;
        setup.config = self._dir_confsetup;
        setup.ROOT = self._dir_mtroot;
        setup.absRoot = self._dir_mtroot;

        setup.gpgImport(setup.cygwinPublicRingUri);
        setup.setup();

        f = open(self._file_setup_ini, "w");
        f.write(self._var_setupIni.contents);
        f.close();

        f = open(self._file_installed_db, "w");
        f.write(setup.installedDbMagic);
        f.close();

        self._var_packagename = self._var_setupIni.pkg.name;
        self._var_files = ["", self._var_packagename];
        self._var_download_p = False;
        self._var_downloads = None;
        self._var_distname = None;
        self._var_nodeps_p = False;
        self._var_regex_search = False;
        self._var_nobarred = False;
        self._var_nopostinstall = False;
        self._var_nopostremove = False;
        self._var_dists = 0;
        self._var_installed = 0;

        self.obj = CygApt(self._var_packagename,
                          self._var_files,
                          self._file_user_config,
                          self._var_cygwin_p,
                          self._var_download_p,
                          self._var_mirror,
                          self._var_downloads,
                          self._var_distname,
                          self._var_nodeps_p,
                          self._var_regex_search,
                          self._var_nobarred,
                          self._var_nopostinstall,
                          self._var_nopostremove,
                          self._var_dists,
                          self._var_installed,
                          self._var_exename,
                          self._var_verbose);

        self.obj.cache = self._dir_execache;
        self.obj.downloadDir = self._dir_downloads;
        self.obj.setup_ini = self._file_setup_ini;
        self.obj.ROOT = self._dir_mtroot;
        self.obj.mirror = self._var_mirror;
        self.obj.installedDb = self._file_installed_db;
        self.obj.config = self._dir_confsetup;

        # set attributes
        self.obj.appName = self._var_exename;
        self.obj.pm.cygwinPlatform = False;
        self.obj.pm.mountRoot = self._dir_mtroot;
        self.obj.pm.root = self._dir_mtroot[:-1];
        self.obj.pm.map = {self._dir_mtroot:self._dir_mtroot};

        expected = self._dir_mtroot;
        ret = self.obj.pm.mapPath(self._dir_mtroot);
        self.assertEqual(ret, expected);
        expected = os.path.join(self._dir_mtroot, "diranme");
        ret = self.obj.pm.mapPath(expected);
        self.assertEqual(ret, expected);

        self.obj.dists = self._var_setupIni.dists.__dict__;
        self.obj.distname = "curr";
        self.obj.ballTarget = "install";
        self.obj.always_update = False;

        self.obj.postInstallDir = self._dir_postinstall;
        self.obj.preremove_dir = self._dir_preremove;
        self.obj.postRemoveDir = self._dir_postremove;

        self.obj.dosBinDir = self._dir_bin;
        self.obj.dosBash = "/usr/bin/bash";
        self.obj.dosLn = "/usr/bin/ln";

        self.obj.prefixRoot = self._dir_mtroot[:-1];
        self.obj.absRoot = self._dir_mtroot;
        self.obj.installed = {0:{}};

        self.obj._forceBarred = [self._var_setupIni.barredpkg.name];

    def test___init__(self):
        self.assertTrue(isinstance(self.obj, CygApt));

    def testWriteFileList(self):
        lst = ["file1", "file2/", "file3/dfd"];
        lstret = [b"file1\n", b"file2/\n", b"file3/dfd\n"];
        gzfile = os.path.join(self._dir_confsetup, "pkg.lst.gz");
        self.obj.config = self._dir_confsetup;
        self.obj.pkgName = "pkg";
        self.obj.setup_ini = self._file_setup_ini;
        self.obj.writeFileList(lst);
        gzf = gzip.open(gzfile);
        expected = gzf.readlines();
        gzf.close();
        self.assertEqual(expected, lstret);

    def testRunScript(self):
        script = "/pkg.sh";
        script_done = script + ".done";
        map_script = self.obj.pm.mapPath(script);
        map_script_done = self.obj.pm.mapPath(script_done);
        f = open(map_script, "w");
        f.write("#!/bin/bash\nexit 0;");
        f.close();

        self.obj.runScript(script, False);
        self.assertTrue(os.path.exists(map_script_done));
        
    def testVersionToString(self):
        versiont = [1,12,3,1];
        out = "1.12.3-1";
        ret = self.obj.versionToString(versiont);
        self.assertEqual(ret, out);
        
    def testStringToVersion(self):
        string = "1.12.3-1";
        out = [1,12,3,1];
        ret = self.obj.stringToVersion(string);
        self.assertEqual(list(ret), out);
        
    def testSplitBall(self):
        input = "pkgball-1.12.3-1.tar.bz2";
        output = ["pkgball", (1,12,3,1)];
        ret = self.obj.splitBall(input);
        self.assertEqual(list(ret), output);
        
    def testJoinBall(self):
        input = ["pkgball", [1,12,3,1]];
        output = "pkgball-1.12.3-1";
        ret = self.obj.joinBall(input);
        self.assertEqual(ret, output);
        
    def testGetSetupIni(self):
        self.obj.dists = 0;
        self.obj.getSetupIni();
        self.assertEqual(self.obj.dists, self._var_setupIni.dists.__dict__);

    def testGetUrl(self):
        ret = self.obj.getUrl();
        filename, size, md5 = self._var_setupIni.pkg.install.curr.toString().split(
                                           " ",
                                           3);

        self.assertEqual(ret, (filename, md5));

    #test also doDownload ball getmd5 and md5
    def testDownload(self):
        self.obj.download();
        filename = os.path.join(self._dir_downloads,
                                self._var_setupIni.pkg.install.curr.url);

        self.assertTrue(os.path.exists(filename));

    def testGetRequires(self):
        expected = self._var_setupIni.pkg.requires.split(" ");
        ret = self.obj.getRequires();

        self.assertEqual(ret, expected);

    def testGetInstalled(self):
        pkg = ['pkgname', 'pkgname-1.1-1.tar.bz2', "0"];
        f = open(self._file_installed_db, "a");
        f.write(" ".join(pkg));
        f.close();

        expected = {int(pkg[2]):{pkg[0]:pkg[1]}};

        self.obj.installed = 0;
        ret = self.obj.getInstalled();

        self.assertEqual(ret, expected);

    def testWriteInstalled(self):
        pkg = ['pkgname', 'pkgname-1.1-1.tar.bz2', "0"];
        expected = self.obj.installedDbMagic;
        expected += " ".join(pkg);

        self.obj.installed = {int(pkg[2]):{pkg[0]:pkg[1]}};

        self.obj.writeInstalled();
        f = open(self._file_installed_db);
        ret = f.read();
        f.close();

        self.assertEqual(ret.replace("\n", ""), expected.replace("\n", ""));

    def testGetField(self):
        expected = self._var_setupIni.pkg.category;
        ret = self.obj.getField("category");
        self.assertEqual(ret, expected);

    def testGetVersion(self):
        expected = self._var_setupIni.pkg.version.curr;
        expected = expected.replace(".", "").replace("-", "");
        expected = list(expected);
        i = 0;
        for val in expected:
            expected[i] = int(val);
            i = i + 1;
        del i;
        expected = tuple(expected);

        ret = self.obj.getVersion();
        self.assertEqual(ret, expected);

    def testSearch(self):
        self.obj.pkgName = "libp";

        expected = self._var_setupIni.libpkg.name + \
                   " - " + \
                   self._var_setupIni.libpkg.shortDesc.replace('"','') + \
                   "\n";

        ob = CygAptOb(True);
        self.obj.search();
        ret = ob.getClean();

        self.assertEqual(ret, expected);

    def testGetMissing(self):
        expected = self._var_setupIni.pkg.requires.split(" ");
        expected.append(self.obj.pkgName);
        ret = self.obj.getMissing();

        self.assertEqual(ret, expected);

    def testDoInstall(self):
        self.testDownload();
        self.obj.doInstall();
        self.assertInstall([self.obj.pkgName]);

    def testDoInstallExternal(self):
        self.testDownload();
        self.obj.cygwinPlatform = False;
        self.obj.doInstall();
        self.assertInstall([self.obj.pkgName]);


    def testPostInstall(self):
        self.testDoInstall();
        self.obj.postInstall();
        self.assertPostInstall();

    def testGetFileList(self):
        self.testDoInstall();
        expected = self._var_setupIni.pkg.filelist;
        ret = self.obj.getFileList();
        self.assertEqual(ret.sort(), expected.sort());

    def testDoUninstall(self):
        self.testPostInstall();
        self.obj.doUninstall();
        self.assertRemove([self.obj.pkgName]);

    def testInstall(self):
        # INSTALL
        self.obj.install();

        expected = self._var_setupIni.pkg.requires.split(" ");
        expected.append(self.obj.pkgName);
        self.assertInstall(expected);
        self.assertPostInstall();

    def testRemove(self):
        self.testInstall();
        # REMOVE
        self.obj.remove();
        self.assertRemove([self.obj.pkgName]);

    def testUpgrade(self):
        self.testInstall();
        pkgname = self._var_setupIni.pkg.name;
        version_file = os.path.join(self._dir_mtroot,
                                    "var",
                                    pkgname,
                                    "version");
        f = open(version_file);
        retcurr = f.read();
        f.close();

        self.obj.distname = "test";
        self.obj.upgrade();

        expected = self._var_setupIni.pkg.version.test;
        f = open(version_file);
        rettest = f.read();
        f.close();
        self.assertNotEqual(retcurr, rettest);

    def testPurge(self):
        self.testPostInstall();
        self.obj.purge();
        self.assertRemove([self.obj.pkgName]);

        self.assertFalse(os.path.exists(self.obj.getBall()));

    def testSource(self):
        os.chdir(self._dir_user);
        self.assertRaises(SystemExit, self.obj.source);
        self.assertTrue(os.path.isdir(self.obj.pkgName));

    def testFind(self):
        self.testDoInstall();

        self.obj.pkgName = "version";

        pkgname = self._var_setupIni.pkg.name;
        expected = pkgname + ": " + os.path.join("/var",
                                    pkgname,
                                    "version") + "\n";

        ob = CygAptOb(True);
        self.obj.find();
        ret = ob.getClean();
        self.assertEqual(ret, expected);

    def testIsBarredPackage(self):
        self.assertTrue(self.obj.isBarredPackage(self._var_setupIni.libbarredpkg.name));
        self.assertTrue(self.obj.isBarredPackage(self._var_setupIni.barredpkg.name));
        self.assertFalse(self.obj.isBarredPackage(self._var_setupIni.libpkg.name));
        self.assertFalse(self.obj.isBarredPackage(self._var_setupIni.pkg.name));
        self.obj.isBarredPackage("not_exists_pkg");

    def assertInstall(self, pkgname_list):
        pkg_ini_list = [];
        for pkg in pkgname_list:
            pkg_ini_list.append(self._var_setupIni.__dict__[pkg]);

        for pkg in pkg_ini_list:
            f = gzip.open(os.path.join(self._dir_confsetup,
                                  "{0}.lst.gz".format(pkg.name)));
            lines = f.readlines();
            f.close();
            self.assertEqual(pkg.filelist.sort(), lines.sort());
            for filename in pkg.filelist:
                filename = self._dir_mtroot + filename;
                if os.path.dirname(filename) != self._dir_postinstall:
                    self.assertTrue(os.path.exists(filename),
                                    filename + " not exists");

    def assertPostInstall(self):
        for filename in os.listdir(self._dir_postinstall):
            if filename[-3:] == ".sh":
                self.assertTrue(False, filename + " runing fail");

    def assertRemove(self, pkgname_list):
        pkg_ini_list = [];
        for pkgname in pkgname_list:
            pkg_ini_list.append(self._var_setupIni.__dict__[pkgname]);

        for pkg in pkg_ini_list:
            for filename in pkg.filelist:
                if filename[-1] != "/":
                    filename = self._dir_mtroot + filename;
                    self.assertFalse(os.path.exists(filename),
                                     filename + " exists");

            for filename in os.listdir(self._dir_preremove):
                if filename == pkg.name + ".sh":
                    self.assertTrue(False, filename + " preremove runing fail");

            for filename in os.listdir(self._dir_postremove):
                if filename == pkg.name + ".sh":
                    self.assertTrue(False, filename + " postremove runing fail");

if __name__ == "__main__":
    unittest.main();
