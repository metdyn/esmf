# $Id$

"""
decorators
"""

#### DECORATORS #########################################################

import warnings
import functools

from ESMF.api.constants import LogKind

try:
    import nose

    def expected_failure(test):
        @functools.wraps(test)
        def inner(*args, **kwargs):
            try:
                test(*args, **kwargs)
            except Exception:
                raise nose.SkipTest
        return inner
except:
    def expected_failure(test):
        @functools.wraps(test)
        def inner(*args, **kwargs):
            try:
                test(*args, **kwargs)
            except:
                raise AssertionError('SkipTest: Failure expected')
        return inner


def deprecated(func):
    '''This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.  Other decorators must be upper.'''

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.warn_explicit(
            "Call to deprecated function {}.".format(func.__name__),
            category=DeprecationWarning,
            filename=func.func_code.co_filename,
            lineno=func.func_code.co_firstlineno + 1
        )
        return func(*args, **kwargs)
    return new_func

def initialize(func):
    '''This is a decorator which can be used to initialize ESMF, by
    creating a Manager object, if it has not already been done.'''

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        from ESMF.api import esmpymanager

        esmp = esmpymanager.Manager(logkind = LogKind.SINGLE, debug = False)
        return func(*args, **kwargs)
    return new_func
