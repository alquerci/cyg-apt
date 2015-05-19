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

import os;
import re;
import shutil;
import struct;
import sys;
import tarfile;
import urlparse;
import stat;
import warnings;

from cygapt.exception import ApplicationException;
from cygapt.exception import InvalidArgumentException;
from cygapt.exception import UnexpectedValueException;
from cygapt.url_opener import CygAptURLopener;
from cygapt.structure import ConfigStructure;
from cygapt.process import Process;
from cygapt.process.exception import ProcessFailedException;

def cygpath(path):
    p = Process(["cygpath", path]);
    p.run();
    dospath = p.getOutput().strip();
    return dospath;

def parse_rc(cyg_apt_rc):
    """Parse the user configuration file.

    @param cyg_apt_rc: str The path to the user configuration.

    @return: ConfigStructure The configuration.
    """
    f = open(cyg_apt_rc);
    lines = f.readlines();
    f.close();
    rc_regex = re.compile(r"^\s*(\w+)\s*=\s*(.*)\s*$");
    always_update = False;
    config = ConfigStructure();
    for i in lines:
        result = rc_regex.search(i);
        if result:
            k = result.group(1);
            v = result.group(2);
            if k in config.__dict__ :
                config.__dict__[k] = str(v).rstrip().strip('\'"');
            if 'setup_ini' == k :
                warnings.warn(
                    "The configuration field `setup_ini` is deprecated"
                    " since version 1.1 and will be removed in 2.0.",
                    DeprecationWarning,
                );

    if config.always_update in [True, 'True', 'true', 'Yes', 'yes']:
        always_update = True;
    else:
        always_update = False;

    config.always_update = always_update;

    return config;

def remove_if_exists(fn):
    try:
        os.remove(fn);
    except OSError:
        pass;

def open_tarfile(ball, xzPath='xz'):
    """Opens a tar file like `tarfile.open`.

    Supports also LZMA compressed tarballs.

    @param ball:   str A tar file, it can be compressed
    @param xzPath: str A path to the lzma program

    @return: TarFile An appropriate TarFile instance
    """
    assert isinstance(xzPath, str);

    ball_orig = ball;
    if ball.lower().endswith('.tar.xz'):
        ball_orig = ball;
        ball = ball[:-3]; # remove .xz extension
        remove_if_exists(ball);
        Process([xzPath, '-k', '-d', ball_orig]).mustRun();
        # an empty tarball is valid
        if 0 == os.path.getsize(ball) :
            with tarfile.open(ball, 'w'):
                pass;
    try:
        tf = tarfile.open(ball);
    except tarfile.TarError:
        if ball_orig != ball:
            remove_if_exists(ball);

        raise;

    if ball_orig != ball:
        tf_close_orig = tf.close;
        def tf_close():
            retValue = tf_close_orig();
            remove_if_exists(ball);
            return retValue;
        tf.close = tf_close;
    return tf;

def is_tarfile(ball, xzPath='xz'):
    try:
        open_tarfile(ball, xzPath).close();
        return True;
    except tarfile.TarError:
        return False;
    except ProcessFailedException:
        return False;

def prsort(lst):
    lst.sort();
    lst.reverse();
    return lst;

def rename(src, dest):
    if os.path.exists(dest):
        os.remove(dest);
    os.rename(src, dest);

def rmtree(path):
    """Removes the given path without following symlinks.

    It can remove directory content also if it does not have permissions.

    @param path: str A link, file or directory path.

    @raise OSError: When the path cannot be removed.
    """
    rmtree_helper(path);

    if os.path.islink(path) or os.path.isfile(path) :
        os.remove(path);

        return;

    if os.path.isdir(path) :
        shutil.rmtree(path);

def rmtree_helper(path):
    """Adds reading and writing permissions for owner for each path recursively.

    @param path: str The path to adding permissions.

    @raise OSError: When permissions cannot be set.
    """
    if os.path.islink(path) :
        return;

    if os.path.exists(path) :
        # Adds reading and writing permissions for owner.
        os.chmod(path, stat.S_IWUSR | stat.S_IRUSR | os.stat(path)[stat.ST_MODE]);

    if os.path.isdir(path) :
        files = os.listdir(path);
        for x in files:
            fullpath = os.path.join(path, x);
            rmtree_helper(fullpath);

def uri_get(directory, uri, verbose=False):
    up = urlparse.urlparse(uri);
    scriptname = os.path.basename(sys.argv[0]);

    if up.scheme == "file":
        shutil.copy(uri[7:], directory);
        if verbose:
            print("cp {0} {1}".format(uri[7:], directory));
    elif up.scheme == "http" or up.scheme == "ftp":
        url_base = os.path.basename(up.path);
        old_cwd = os.getcwd();
        os.chdir(directory);
        if verbose:
            print("\r{0}: downloading: {1}".format(scriptname, uri));
        try:
            opener = CygAptURLopener(verbose);
            opener.retrieve(
                uri,
                "{0}.tmp".format(url_base),
                reporthook=opener.dlProgress
            );
        except IOError:
            opener.setErrorCode(1);
        finally:
            opener.close();

        if opener.getErrorCode() == 200:
            rename(url_base + ".tmp", url_base);
        else:
            if os.path.exists(url_base + ".tmp"):
                os.remove(url_base + ".tmp");
            os.chdir(old_cwd);
            raise RequestException(
                "{0} unreached URL {1}"
                "".format(opener.getErrorCode(), uri)
            );
        os.chdir(old_cwd);
    else:
        raise InvalidArgumentException("bad URL {0}".format(uri));

def pe_is_64_bit(fn):
    """Reads the header of a PE (.exe or .dll) file to determine its
    architecture.

    @param fn: str The PE filename to read.

    @return: bool Whether the PE file is 64-bit.

    @raise UnexpectedValueException: If an invalid value is found.
    @raise IOError: If a read error occurs.
    """
    with open(fn, "rb") as f:
        if "MZ" != f.read(2) :
            raise UnexpectedValueException(
                "File '{0}' is not a DOS executable."
                "".format(fn)
            );
        f.seek(0x3c); # Offset of PE header (e_lfanew in DOS header)
        pe_header = struct.unpack('<L', f.read(4))[0];
        f.seek(pe_header);
        if "PE\0\0" != f.read(4) :
            raise UnexpectedValueException(
                "Could not find PE header in file '{0}'."
                "".format(fn)
            );
        f.seek(pe_header + 0x4); # Machine field of COFF header
        machine = struct.unpack('<H', f.read(2))[0];
        if 0x014c == machine :
            return False;
        elif 0x8664 == machine :
            return True;
        else:
            raise UnexpectedValueException(
                "Bad machine value 0x{0:X} in file '{1}'."
                "".format(machine, fn)
            );

class RequestException(ApplicationException):
    pass;
