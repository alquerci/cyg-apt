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


import os

from . import utils as cautils

class PathMapper:
    def __init__(self, root, cygwin_p):
        self.root = root
        p = os.popen(self.root + "/bin/mount");
        mountout = p.readlines()
        p.close();
        self.mountroot = "/"
        self.add_mapping(mountout)
        self.cygwin_p = cygwin_p

    def add_mapping(self, mtab):
        self.map = {}
        mtab = [l.split() for l in mtab]
        for l in mtab:
            if l[2] != "/":
                self.map[l[2] + "/"] = l[0] + "/"
            else:
                self.mountroot = l[0] + "/"

    def map_path(self, path):
        if self.cygwin_p:
            return path
        # sort to map to /e/bar/foo in pefrence /e/bar
        l = cautils.prsort(list(self.map.keys()))
        for cygpath in l:
            if path.find(cygpath) == 0:
                path = path.replace(cygpath, self.map[cygpath])
                return path
        return self.root + path
