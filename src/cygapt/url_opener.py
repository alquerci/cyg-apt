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


import sys
import urllib.request, urllib.parse, urllib.error

class CygAptURLopener(urllib.request.FancyURLopener):
    def __init__(self, verbose, *args):
        urllib.request.FancyURLopener.__init__(self, *args)
        self.verbose = verbose
        self.errcode = 200
        self.barmax = 40

    def http_error_default(self, url, fp, errcode, errmsg, headers):
        self.errcode = errcode
        return urllib.request.FancyURLopener.http_error_default\
            (self, url, fp, errcode, errmsg, headers)

    def dlProgress(self, count, blockSize, totalSize):
        if self.errcode != 200:
            return
        if not self.verbose:
            return
        barmax = self.barmax
        ratio = min((count * blockSize), totalSize) / float(totalSize)
        bar = int(barmax * ratio)
        if ratio == 1.0:
            sys.stdout.write(" "*70 + "\r")
            sys.stdout.flush()
        else:
            print("[", end="");
            for i in range(barmax):
                if i < bar:
                    sys.stdout.write("=")
                elif i == bar:
                    sys.stdout.write(">")
                else:
                    sys.stdout.write(" ")
            sys.stdout.write("]\r")
            sys.stdout.flush()

