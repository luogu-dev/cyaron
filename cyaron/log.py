from __future__ import print_function
from functools import partial
import sys

_print = print

def _join_dict(a, b):
    """join two dict"""
    c = a.copy()
    for k, v in b.items():
        c[k] = v
    return c

_log_funcs = {}
_log = lambda funcname, *args, **kwargs: _log_funcs.get(funcname, lambda *args, **kwargs: None)(*args, **kwargs)

"""5 log levels
1. debug:   debug info
2. info:    common info
3. print:   print output
4. warn:    warnings
5. error:   errors
"""

debug = partial(_log, 'debug')
info = partial(_log, 'info')
print = partial(_log, 'print')
warn = partial(_log, 'warn')
error = partial(_log, 'error')

def register_logfunc(funcname, func):
    """register logfunc
    str funcname -> name of logfunc
    callable func -> logfunc
    """
    if func is not None:
        _log_funcs[funcname] = func
    else:
        try:
            del _log_funcs[funcname]
        except KeyError:
            pass

_nb_print = lambda *args, **kwargs: _print(*args, **_join_dict(kwargs, {'flush': True}))
_nb_print_e = lambda *args, **kwargs: _print(*args, **_join_dict(kwargs, {'file': sys.stderr, 'flush': True}))

def set_quiet():
    """set log mode to "quiet" """
    register_logfunc('debug', None)
    register_logfunc('info', None)
    register_logfunc('print', _nb_print)
    register_logfunc('warn', None)
    register_logfunc('error', _nb_print_e)

def set_normal():
    """set log mode to "normal" """
    register_logfunc('debug', None)
    register_logfunc('info', _nb_print)
    register_logfunc('print', _nb_print)
    register_logfunc('warn', _nb_print_e)
    register_logfunc('error', _nb_print_e)

def set_verbose():
    """set log mode to "verbose" """
    register_logfunc('debug', _nb_print)
    register_logfunc('info', _nb_print)
    register_logfunc('print', _nb_print)
    register_logfunc('warn', _nb_print_e)
    register_logfunc('error', _nb_print_e)

set_normal()
