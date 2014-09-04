Coding Conventions for cyg-apt
==============================

Extends and overwrite [PEP 8][] and [PEP 257][]

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC 2119][].

[RFC 2119]: http://www.ietf.org/rfc/rfc2119.txt
[PEP 8]: http://www.python.org/dev/peps/pep-0008/
[PEP 257]: http://www.python.org/dev/peps/pep-0257/


General
-------

* Use classes as much as possible.
* A file MAY contain one or many interdependent classes.
* Each statement MUST end with a semicolon `;`.


Idioms
------

* Use only format() method to formatting strings.
* `print` is a function.


Files
-----

* Code MUST use 4 spaces for indenting, not tabs.
* All Python files MUST use the Unix LF (line feed) line ending.
* All Python files MUST end with a single blank line.


Classes
-------

* Class names MUST be declared in `StudlyCaps`.
* Method names MUST be declared in `camelCase`.
* Property/Method names MUST start but not ending with
  TWO underscores `__` to indicate private visibility.
* Property/Method names MUST start but not ending with
  ONE underscores `_` to indicate protected visibility.
* An `exception` module MUST contain all exception classes of the package.
* Every `Exception` class MUST end with `Exception`.
* Every `Interface` class MUST end with `Interface`.


String
------

* Double quotes for text
* Single quotes for anything that behaves like an identifier
* Double quoted raw string literals for regexps
* Tripled double quotes for docstrings


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

        @param dummy: str Some argument description
        @param bar: BarInterface Some argument description
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

    def __transformText(self, dummy, options=None):
        """Transformes the dummy following options.

        @param dummy:   str Some argument description
        @param options: dict Some argument description

        @return: str|None Transformed input

        @raise Exception: When unrecognized dummy option
        """
        assert isinstance(dummy, str);
        assert None is options or isinstance(options, dict);

        mergedOptions = {
            'some_default': "values",
            'another_default': "more values",
        };
        if options :
            mergedOptions.update(options);

        if True is dummy :
            return;

        if "string" == dummy :
            if "values" == mergedOptions['some_default'] :
                return dummy[:5];

            return dummy.title();

        raise Exception('Unrecognized dummy option "{0}"'.format(dummy));

```
