#!@ENV@ @PYTHON@
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

from __future__ import absolute_import;

import sys;
import os;

pkglibdir = os.path.normcase(r'@pkglibdir@').capitalize();
if pkglibdir not in sys.path :
    sys.path.insert(0, pkglibdir);

from cygapt.main import CygAptMain;

if __name__ == "__main__":
    CygAptMain();
