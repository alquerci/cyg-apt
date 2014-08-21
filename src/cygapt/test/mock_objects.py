# -*- coding: utf-8 -*-
# This file is part of the cygapt package.
#
# (c) 2002-2009 Jan Nieuwenhuizen <janneke@gnu.org>
#     2002-2009 Chris Cormie      <cjcormie@gmail.com>
#          2012 James Nylen       <jnylen@gmail.com>
#     2012-2014 Alexandre Quercia <alquerci@email.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.

from __future__ import absolute_import;

import inspect;

class ExpectationFailedException(Exception):
    pass;


class VerifiableInterface():
    def verify(self):
        """
        @raise ExpectationFailedException: When the current expectation not is valid.
        """
        pass;


class InvocationInterface():
    def getParameters(self):
        """
        @return: list [args, kwargs] 
        """


class StubInterface():
    def invoke(self, invocation):
        assert isinstance(invocation, InvocationInterface);


class ReturnStub(StubInterface):
    def __init__(self, value):
        self.__value = value;

    def invoke(self, invocation):
        assert isinstance(invocation, InvocationInterface);
        return self.__value;

    def __str__(self):
        return "return user-specified value {0}".format(self.__value);


class ReturnValueMapStub(StubInterface):
    def __init__(self, valueMap):
        self.__valueMap = valueMap;

    def invoke(self, invocation):
        assert isinstance(invocation, InvocationInterface);
        args, kwargs = invocation.getParameters();
        parametersCount = len(args) + len(kwargs);
        for values in self.__valueMap :
            values = list(values);
            returnValue = values.pop();
            kwargsMap = values.pop();
            argsMap = values;
            if parametersCount != len(argsMap) + len(kwargsMap) :
                continue;
            if (args, kwargs) == (argsMap, kwargsMap) :
                return returnValue;

    def __str__(self):
        return "return value from a map";


class ReturnArgumentStub(StubInterface):
    def __init__(self, argumentIndex):
        self.__argumentIndex = argumentIndex;

    def invoke(self, invocation):
        assert isinstance(invocation, InvocationInterface);
        args, kwargs = invocation.getParameters();
        if self.__argumentIndex in kwargs :
            return kwargs[self.__argumentIndex];
        if self.__argumentIndex < len(args) :
            return args[self.__argumentIndex];
        return None;

    def __str__(self):
        return "return argument #{0:d}".format(self.__argumentIndex);


class ReturnCallbackStub(StubInterface):
    def __init__(self, callback):
        self.__callback = callback;

    def invoke(self, invocation):
        assert isinstance(invocation, InvocationInterface);
        args, kwargs = invocation.getParameters();
        return self.__callback(*args, **kwargs);

    def __str__(self):
        return "return result of user defined callback {0!r} with the passed arguments".format(
            self.__callback,
        );


class ExceptionStub(StubInterface):
    def __init__(self, exception):
        assert isinstance(exception, Exception);
        self.__exception = exception;

    def invoke(self, invocation):
        assert isinstance(invocation, InvocationInterface);
        raise self.__exception;

    def __str__(self):
        return "raise user-specified exception {0}".format(self.__exception);


class InvokableInterface(VerifiableInterface):
    def invoke(self, invocation):
        assert isinstance(invocation, InvocationInterface);

    def matches(self, invocation):
        assert isinstance(invocation, InvocationInterface);


class InvocationMatcherInterface(VerifiableInterface):
    def invoked(self, invocation):
        assert isinstance(invocation, InvocationInterface);

    def matches(self, invocation):
        assert isinstance(invocation, InvocationInterface);


class MatcherCollectionInterface():
    def addMatcher(self, invocationMatcher):
        assert isinstance(invocationMatcher, InvocationMatcherInterface);


class Matcher(InvocationMatcherInterface):
    def __init__(self, invocationMatcher):
        assert isinstance(invocationMatcher, InvocationMatcherInterface);
        self.parametersMatcher = AnyParametersMatcher();
        self.stub = None;
        self.invocationMatcher = invocationMatcher;

    def invoked(self, invocation):
        assert isinstance(invocation, InvocationInterface);
        self.invocationMatcher.invoked(invocation);
        try:
            if self.parametersMatcher :
                if self.parametersMatcher.matches(invocation) :
                    self.parametersMatcher.verify();
        except ExpectationFailedException as e:
            raise ExpectationFailedException("{0}\n{1}".format(
                self.invocationMatcher,
                e,
            ));
        if self.stub :
            return self.stub.invoke(invocation);

    def matches(self, invocation):
        assert isinstance(invocation, InvocationInterface);
        if not self.invocationMatcher.matches(invocation) :
            return False;
        return True;

    def verify(self):
        try:
            self.invocationMatcher.verify();
            if self.parametersMatcher :
                self.parametersMatcher.verify();
        except ExpectationFailedException as e:
            raise ExpectationFailedException("{0}\n{1}".format(
                self.invocationMatcher,
                e,
            ));

    def __str__(self):
        text = list();
        if self.invocationMatcher :
            text.append(str(self.invocationMatcher));
        if self.parametersMatcher :
            text.append("where "+str(self.parametersMatcher));
        if self.stub :
            text.append("will "+str(self.stub));
        return " ".join(text);


class StatelessInvocationMatcher(InvocationMatcherInterface):
    def invoked(self, invocation):
        assert isinstance(invocation, InvocationInterface);

    def matches(self, invocation):
        assert isinstance(invocation, InvocationInterface);


class InvokedRecorderMatcher(InvocationMatcherInterface):
    def __init__(self):
        self.__invocations = list();

    def getInvocationCount(self):
        return len(self.__invocations);

    def getInvocations(self):
        return self.__invocations;

    def hasBeenInvoked(self):
        return bool(self.__invocations);

    def invoked(self, invocation):
        assert isinstance(invocation, InvocationInterface);
        self.__invocations.append(invocation);

    def matches(self, invocation):
        assert isinstance(invocation, InvocationInterface);
        return True;


class AnyInvokedCountMatcher(InvokedRecorderMatcher):
    def verify(self):
        pass;

    def __str__(self):
        return "invoked zero or more times";


class InvokedAtLeastOnceMatcher(InvokedRecorderMatcher):
    def verify(self):
        if self.getInvocationCount() < 1 :
            raise ExpectationFailedException('Expected invocation at least once but it never occured.');

    def __str__(self):
        return "invoked at least once";


class InvokedCountMatcher(InvokedRecorderMatcher):
    def __init__(self, expectedCount):
        InvokedRecorderMatcher.__init__(self); 
        self.__expectedCount = expectedCount;

    def verify(self):
        count = self.getInvocationCount();
        if self.__expectedCount != count :
            raise ExpectationFailedException('Method was expected to be called {0:d} times, actually called {1:d} times.'.format(
                self.__expectedCount,
                count
            ));

    def __str__(self):
        return "invoked {0:d} time{1}".format(
            self.__expectedCount,
            "s" if 1 < self.__expectedCount else "",
        );


class ObjectInvocation(InvocationInterface):
    def __init__(self, className, methodName, args, kwargs, obj):
        self.__args = list(args);
        self.__kwargs = dict(kwargs);
        self.__className = className;
        self.__methodName = methodName;
        self.__object = obj;

    def getParameters(self):
        return [self.__args, self.__kwargs];

    def __str__(self):
        parameters = list();
        for value in self.__args :
            parameters.append('{0!r}'.format(value));
        for name, value in self.__kwargs :
            parameters.append('{0} = {1!r}'.format(name, value));
        return '{0}.{1}({2})'.format(
            self.__className,
            self.__methodName,
            ','.join(parameters)
        );


class ConstraintInterface():
    def evaluate(self, value):
        """
        @return: Boolean
        """


class IsEqualConstraint(ConstraintInterface):
    def __init__(self, expected):
        self.__expected = expected;

    def evaluate(self, value):
        return self.__expected == value;

    def __str__(self):
        return "is equal to {0}".format(self.__expected);


class AnyParametersMatcher(StatelessInvocationMatcher):
    def matches(self, invocation):
        assert isinstance(invocation, InvocationInterface);
        return True;

    def __str__(self):
        return "with any parameters";


class ParametersMatcher(StatelessInvocationMatcher):
    def __init__(self, args, kwargs):
        self.__args = list();
        self.__kwargs = dict();
        self.__invocation = None;
        for arg in args :
            if not isinstance(arg, ConstraintInterface) :
                arg = IsEqualConstraint(arg);
            self.__args.append(arg);
        for name, value in kwargs :
            if not isinstance(value, ConstraintInterface) :
                value = IsEqualConstraint(value);
            self.__kwargs[name] = value;

    def matches(self, invocation):
        assert isinstance(invocation, InvocationInterface);
        self.__invocation = invocation;
        self.verify();
        args, kwargs = invocation.getParameters();
        return len(self.__args) > len(args) or len(self.__kwargs) > len(kwargs);

    def verify(self):
        args, kwargs = self.__invocation.getParameters();
        if len(self.__args) > len(args) or len(self.__kwargs) > len(kwargs) :
            raise ExpectationFailedException('Parameter count for invocation {0} is too low.'.format(
                self.__invocation
            ));
        i = 0;
        for arg in self.__args :
            if not arg.evaluate(args[i]) :
                raise ExpectationFailedException('Parameter {0:d} for invocation {1} does not match expected value.'.format(
                    i,
                    self.__invocation
                ));
            i += 1;
        for name, value in self.__kwargs :
            if not value.evaluate(kwargs[name]) :
                raise ExpectationFailedException('Parameter {0} for invocation {1} does not match expected value.'.format(
                    name,
                    self.__invocation
                ));
            i += 1;

    def __str__(self):
        parameters = list();
        i = 0;
        for value in self.__args :
            parameters.append('{0:d} {1}'.format(i, value));
            i += 1;
        for name, value in self.__kwargs :
            parameters.append('{0} {1}'.format(name, value));
        return "with parameter{0} {1}".format(
            "s" if 1 < len(parameters) else "",
            ' and '.join(parameters),
        );


class InvocationMockerBuilder():
    def __init__(self, collection, invocationMatcher):
        assert isinstance(collection, MatcherCollectionInterface);
        assert isinstance(invocationMatcher, InvocationMatcherInterface);
        self.__collection = collection;
        self.__matcher = Matcher(invocationMatcher);
        self.__collection.addMatcher(self.__matcher);

    def will(self, stub):
        assert isinstance(stub, StubInterface);
        self.__matcher.stub = stub;
        return self;

    def calledWith(self, *args, **kwargs):
        self.__matcher.parametersMatcher = ParametersMatcher(args, kwargs);
        return self;


class InvocationMocker(MatcherCollectionInterface, InvokableInterface):
    def __init__(self, methodName):
        self.__matchers = list();
        self.__methodName = methodName;

    def expects(self, invocationMatcher):
        assert isinstance(invocationMatcher, InvocationMatcherInterface);
        return InvocationMockerBuilder(self, invocationMatcher);

    def addMatcher(self, invocationMatcher):
        assert isinstance(invocationMatcher, InvocationMatcherInterface);
        self.__matchers.append(invocationMatcher);

    def invoke(self, invocation):
        assert isinstance(invocation, InvocationInterface);
        returnValue = None;
        exception = None;
        hasReturnValue = False;
        for matcher in self.__matchers :
            try:
                if matcher.matches(invocation) :
                    value = matcher.invoked(invocation);
                    if not hasReturnValue :
                        returnValue = value;
                        hasReturnValue = True;
            except Exception as e :
                exception = e;
        if exception :
            if isinstance(exception, ExpectationFailedException) :
                raise ExpectationFailedException("Expectation failed for method name {0!r} when {1}".format(
                    self.__methodName,
                    exception,
                ));
            raise;
        return returnValue;

    def verify(self):
        exception = None;
        for matcher in self.__matchers :
            try:
                matcher.verify();
            except Exception as e :
                exception = e;
        if exception :
            if isinstance(exception, ExpectationFailedException) :
                raise ExpectationFailedException("Expectation failed for method name {0!r} when {1}".format(
                    self.__methodName,
                    exception,
                ));
            raise;


class MockMethodInterface(VerifiableInterface):
    def expects(self, invocationMatcher):
        assert isinstance(invocationMatcher, InvocationMatcherInterface);


class MethodMocker(MockMethodInterface):
    def __init__(self, className, methodName, obj):
        self.__className = className;
        self.__methodName = methodName;
        self.__object = obj;
        self.__invocationMocker = None;

    def __call__(self, *args, **kwargs):
        return self.getInvocationMocker().invoke(ObjectInvocation(
            self.__className,
            self.__methodName,
            args,
            kwargs,
            self.__object
        ));

    def expects(self, invocationMatcher):
        assert isinstance(invocationMatcher, InvocationMatcherInterface);
        return self.getInvocationMocker().expects(invocationMatcher);

    def verify(self):
        self.getInvocationMocker().verify();

    def getInvocationMocker(self):
        if None is self.__invocationMocker :
            self.__invocationMocker = InvocationMocker(self.__methodName);
        return self.__invocationMocker;


class MockGenerator(VerifiableInterface):
    _methodMocks = list();

    @classmethod
    def generate(cls, classType):
        class Mock(classType):
            def __init__(self):
                # rename the class name
                self.__class__.__name__ = 'Mock_'+classType.__name__;
                # extends all methods with an instance of MethodMocker
                members = inspect.getmembers(classType);
                for name, value in members :
                    if inspect.ismethod(value) :
                        mock = cls.generateMethodMock(classType.__name__, name, self);
                        setattr(self, name, mock);
        return Mock();

    @classmethod
    def generateMethodMock(cls, className, methodName, obj):
        mock = MethodMocker(className, methodName, obj);
        MockGenerator._methodMocks.append(mock);
        return mock;

    @classmethod
    def verify(cls):
        for mock in MockGenerator._methodMocks :
            mock.verify();

    @classmethod
    def cleanup(cls):
        MockGenerator._methodMocks = list();
