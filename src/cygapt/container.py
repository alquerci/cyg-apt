# -*- coding: utf-8 -*-
# This file is part of the cygapt package.
#
# (c) Alexandre Quercia <alquerci@email.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.

from __future__ import absolute_import;

from cygapt.exception import InvalidArgumentException;

"""
"""

class Container():
    def __init__(self):
        self._services = dict();
        self._parameters = dict();
        self.__loading = dict();

    def set(self, name, service):
        name = str(name).lower();

        self._services[name] = service;

        return self;

    def get(self, name):
        name = str(name).lower();

        # The given value name has actually been initialized
        if self._services.has_key(name) :
            return self._services[name];

        method = getattr(self, 'get'+self.camelize(name)+'Service', None);
        if not (method and isinstance(method, type(self.get))) :
            raise InvalidArgumentException(
                'You have requested a non-existent service "{0}".'.format(name)
            );

        # Checks for circular reference
        if self.__loading.has_key(name) :
            raise RuntimeError(
                'Circular reference detected for service "{0}", path: "{1}".'
                ''.format(name, ' -> '.join(self.__loading.keys()))
            );

        self.__loading[name] = True;
        try:
            service = method();
        except Exception as e :
            self.__loading.pop(name);

            if self._services.has_key(name) :
                self._services.pop(name);

            raise e;
        self.__loading.pop(name);

        return service;

    def getParameter(self, name):
        return self._parameters[str(name).lower()];

    @classmethod
    def camelize(cls, name):
        name = str(name).replace('_', ' ').replace('.', '_ ');
        name = name.replace('\\', '_ ').title().translate(None, ' ');

        return name;
