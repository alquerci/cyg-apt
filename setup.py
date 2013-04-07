#!/usr/bin/python
# -*- coding: utf-8 -*-
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

from __future__ import absolute_import;

from distutils.core import setup;
import os;

__DIR__ = os.path.dirname(os.path.abspath(__file__));

try:
    version = os.environ['VERSION'];
except KeyError:
    version = "2.0.0-DEV";

try:
    pkgname = os.environ['PYPKG'];
except KeyError:
    pkgname = "cygapt";

f = open(__DIR__ + "/README.md");
long_description = f.read();
f.close();

setup(
    name=pkgname,
    package_dir={'': 'src'},
    packages=[pkgname],
    package_data={pkgname: ['LICENSE']},
    version=version,
    description="A Cygwin command line package management tool.",
    long_description=long_description,
    license="GPL-3.0",
    url="https://github.com/nylen/cyg-apt",
    author="Jan Nieuwenhuizen, Chris Cormie, James Nylen, Alexandre Quercia",
    author_email="cjcormie@gmail.com, janneke@gnu.org, jnylen@gmail.com, alquerci@email.com",
    maintainer="Alexandre Quercia",
    maintainer_email="alquerci@email.com",
    platforms="cygwin",
    classifiers=[
        'Development Status :: 1 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License, Version 3',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
    ],
);
