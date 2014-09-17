Coding Conventions for cyg-apt
==============================

Extends and overwrite [PEP 8][] and [PEP 257][]

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC 2119][].

[RFC 2119]: http://www.ietf.org/rfc/rfc2119.txt
[PEP 8]: http://www.python.org/dev/peps/pep-0008/
[PEP 257]: http://www.python.org/dev/peps/pep-0257/


Files
-----

* Code MUST use 4 spaces for indenting, not tabs.
* All Python files MUST use the Unix LF (line feed) line ending.
* All Python files MUST end with a single blank line.
* A file MAY contain one or many interdependent classes.
* An `exception` module MUST contain all exception classes of a package.


Structure
---------

* Each statement MUST end with a semicolon `;`;

* Add a single space after each comma delimiter;

* For sequence types (`dict`, `list`, ...) in a multi-line form, add a comma
  after each item, even the last one;

* Add a blank line before `return` statements, unless the return is alone inside
  a statement-group (like an `if` statement);

* Use classes as much as possible;

* Declare public methods first, then protected ones and finally private ones.
  The exceptions to this rule are the class constructor and the `setUp` and `tearDown` methods
  of unittest tests, which SHOULD always be the first methods to increase readability;

* Strings SHOULD be concatenated using the `format()` method;

* Use `print()` as a function with `from __future__ import print_function;`
  on top of the module;


Naming Conventions
------------------

* Use StudlyCaps for class names;

* Use camelCase, not underscores, for variable, function, method, and argument names;

* Use underscores for option names and parameter names;

* Prefix abstract classes with `Abstract`;

* Suffix interfaces with `Interface`;

* Suffix exceptions with `Exception`;

* Property and method names SHOULD NOT end with an underscore `_`;

* Prefix property and method names with `_` to indicate protected visibility;

* Prefix property and method names with `__` to indicate private visibility;

* Use lowercase alphanumeric characters and underscores for file names;


String Delimiters
-----------------

* Double quotes for text

* Single quotes for anything that behaves like an identifier

* Double quoted raw string literals for regexps

* Tripled double quotes for docstrings


Documentation
-------------

* Add EpyDoc blocks for all classes, methods, and functions;

* Omit the `@return` tag if the method does not return anything;

* The `@param`, `@return` and `@raise` annotations SHOULD only be used;


License
-------

* Cyg-apt is released under the GNU GPLv3 license, and the license block has to be present
  at the top of every Python file, before the first import.


Example
-------

Since a picture - or some code - is worth a thousand words, here's a short example containing most features described below:

```Python
# -*- coding: utf-8 -*-
######################## BEGIN LICENSE BLOCK ########################
# This file is part of the cygapt package.
#
# Copyright (C) 2002-2009 Jan Nieuwenhuizen <janneke@gnu.org>
#               2002-2009 Chris Cormie <cjcormie@gmail.com>
#                    2012 James Nylen <jnylen@gmail.com>
#               2012-2014 Alexandre Quercia <alquerci@email.com>
#
# For the full copyright and license information, please view the
# LICENSE file that was distributed with this source code.
######################### END LICENSE BLOCK #########################

class BarInterface():
    """Coding standards demonstration.
    """

    def getValue(self):
        """Gets a value.

        @return: str The value
        """

class FooBar(BarInterface):
    """Coding standards demonstration.
    """

    SOME_CONST = 42;

    def __init__(self, dummy, bar=None):
        """Constructor.

        @param dummy: str          Some argument description
        @param bar:   BarInterface Some argument description
        """
        assert isinstance(dummy, str);
        assert None is bar or isinstance(bar, BarInterface);

        # define a private property
        self.__fooBar = bar.getValue() if bar else self.__transformText(dummy);

    def getValue(self):
        """Gets a value.

        @return: str The value
        """
        return self.__fooBar;

    def __transformText(
        self,
        dummy,
        some_default="values",
        another_default="more values",
        third_default="more and more values",
    ):
        """Transforms the dummy following options.

        @param dummy:           str Some argument description
        @param some_default:    str Some argument description
        @param another_default: str Some long argument description
                                    with some useful explication
        @param third_default:   str Some argument description

        @return: str|None Transformed input

        @raise Exception: When unrecognized dummy option
        """
        assert isinstance(dummy, str);
        assert isinstance(some_default, str);
        assert isinstance(another_default, str);
        assert isinstance(third_default, str);

        if True is dummy :
            return;

        if "string" == dummy :
            if "values" == some_default :
                return dummy[:5];

            return dummy.title();

        raise Exception('Unrecognized dummy option "{0}"'.format(dummy));

```
