"""
  cyg-apt - a Cygwin package manager.
  
  (c) 2002--2009 Chris Cormie         Jan Nieuwenhuizen
                 <cjcormie@gmail.com> <janneke@gnu.org> 
  (c) 2012       James Nylen
                 <jnylen@gmail.com>
  
  License: GNU GPL
"""

import sys
from cStringIO import StringIO

class CygAptOb:
    """ Output Buffering Control (like php)
    The Output Control functions allow you to control
    when output is sent from the script.
    """
    def __init__(self, start=False):
        self._state = False
        self._buffer = None
        self._value = None
        self._stdout = None
        if start:
            self.start()

    def start(self):
        """ Turn on output buffering """
        self._stdout = sys.stdout
        sys.stdout = StringIO()
        self._buffer = sys.stdout
        self._state = True
        self._value = None

    def end(self):
        """ Turn off output buffering """
        if self._state:
            self._buffer.close()
            self._buffer = None
            sys.stdout = self._stdout
            self._state = False

    def flush(self):
        """ Flush (send) the output buffer """
        self.clean()
        if self._value:
            self._stdout.write(self._value)
        self._value = None

    def get_flush(self):
        """ Flush the output buffer,
            return it as a string and turn off output buffering
        """
        self.clean()
        self.end()
        return self._value

    def end_flush(self):
        """ Flush (send) the output buffer and turn off output buffering """
        self.flush()
        self.end()

    def clean(self):
        """ Clean (erase) the output buffer """
        if self._state:
            self._value = self._buffer.getvalue()
            self._buffer.truncate(0)

    def get_clean(self):
        """ Get current buffer contents and delete current output buffer """
        if not self._state:
            return False

        content = self.get_contents()
        self.end_clean()
        return content

    def end_clean(self):
        """ Clean (erase) the output buffer and turn off output buffering """
        self._value = None
        self.end()

    def implicit_flush(self, flag=True):
        """ Turn implicit flush on/off """
        if flag and self._state:
            self.end()
        elif not flag and not self._state:
            self.start()

    def get_contents(self):
        """ Return the contents of the output buffer """
        if not self._state:
            return False
        
        buf = self._buffer.getvalue()
        if buf:
            self._value = buf
        return self._value

    def get_length(self):
        """ Return the length of the output buffer """
        if not self._state:
            return False

        return len(self.get_contents())