from __future__ import print_function
from functools import partial
import sys
from threading import Lock
try:
    import colorful
except ImportError:
    class colorful:
        def __getattr__(self, attr):
            return lambda st: st
    colorful = colorful()
from .utils import make_unicode

__print = print
def _print(*args, **kwargs):
    flush = False
    if 'flush' in kwargs:
        flush = kwargs['flush']
        del kwargs['flush']
    __print(*args, **kwargs)
    if flush:
        kwargs.get('file', sys.stdout).flush()

def _join_dict(a, b):
    """join two dict"""
    c = a.copy()
    for k, v in b.items():
        c[k] = v
    return c

_log_funcs = {}
_log_lock = Lock()
def log(funcname, *args, **kwargs):
    """log with log function specified by ``funcname``"""
    _log_lock.acquire()
    rv = _log_funcs.get(funcname, lambda *args, **kwargs: None)(*args, **kwargs)
    _log_lock.release()
    return rv

"""5 log levels
1. debug:   debug info
2. info:    common info
3. print:   print output
4. warn:    warnings
5. error:   errors
"""

debug = partial(log, 'debug')
info = partial(log, 'info')
print = partial(log, 'print')
warn = partial(log, 'warn')
error = partial(log, 'error')

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
_cl_print = lambda color, *args, **kwargs: _nb_print(*[color(make_unicode(item)) for item in args], **kwargs) if sys.stdout.isatty() else _nb_print(*args, **kwargs)
_cl_print_e = lambda color, *args, **kwargs: _nb_print_e(*[color(make_unicode(item)) for item in args], **kwargs) if sys.stderr.isatty() else _nb_print_e(*args, **kwargs)

_default_debug = partial(_cl_print, colorful.cyan)
_default_info = partial(_cl_print, colorful.blue)
_default_print = _nb_print
_default_warn = partial(_cl_print_e, colorful.yellow)
_default_error = partial(_cl_print_e, colorful.red)

disp_status="unknown"
bin_status=0

def set_quiet():
    """set log mode to "quiet" """
    global disp_status, bin_status
    register_logfunc('debug', None)
    register_logfunc('info', None)
    register_logfunc('print', _default_print)
    register_logfunc('warn', None)
    register_logfunc('error', _default_error)
    disp_status = "cyaron_preset_quiet"
    bin_status = 0b10100

def set_normal():
    """set log mode to "normal" """
    global disp_status, bin_status
    register_logfunc('debug', None)
    register_logfunc('info', _default_info)
    register_logfunc('print', _default_print)
    register_logfunc('warn', _default_warn)
    register_logfunc('error', _default_error)
    disp_status = "cyaron_preset_normal"
    bin_status = 0b11110

def set_verbose():
    """set log mode to "verbose" """
    global disp_status, bin_status
    register_logfunc('debug', _default_debug)
    register_logfunc('info', _default_info)
    register_logfunc('print', _default_print)
    register_logfunc('warn', _default_warn)
    register_logfunc('error', _default_error)
    disp_status = "cyaron_preset_verbose"
    bin_status = 0b11111

custom_disp_status = "unknown"
def _mode_check(mode, bit, long, short, name, handler):
    global custom_disp_status, bin_status
    if short in mode or long in mode:
        register_logfunc(name, handler)
        custom_disp_status += short
        bin_status |= bit
    else:
        register_logfunc(name, None)
        bin_status &= ~bit
def set_custom(mode):
    """custom mode, use it like ["print","error"] or "pe" for short. """
    global disp_status, custom_disp_status
    custom_disp_status = ""
    _mode_check(mode, 1, 'debug', 'd', 'debug', _default_debug)
    _mode_check(mode, 2, 'info', 'i', 'info', _default_info)
    _mode_check(mode, 4, 'print', 'p', 'print', _default_print)
    _mode_check(mode, 8, 'warn', 'w', 'warn', _default_warn)
    _mode_check(mode, 16, 'error', 'e', 'error', _default_error)
    disp_status = "cyaron_custom_" + custom_disp_status

def _bin_mode_check(mode, bit, short, name, handler):
    global custom_disp_status
    if (mode & bit) != 0:
        register_logfunc(name, handler)
        custom_disp_status += short
    else:
        register_logfunc(name, None)
def set_bin(mode):
    """custom binary mode. available bits are: 1 - debug; 2 - info; 4 - print; 8 - warn; 16 - error"""
    global disp_status, custom_disp_status, bin_status
    custom_disp_status = ""
    bin_status = mode
    _bin_mode_check(mode, 1, 'd', 'debug', _default_debug)
    _bin_mode_check(mode, 2, 'i', 'info', _default_info)
    _bin_mode_check(mode, 4, 'p', 'print', _default_print)
    _bin_mode_check(mode, 8, 'w', 'warn', _default_warn)
    _bin_mode_check(mode, 16, 'e', 'error', _default_error)
    disp_status = "cyaron_custom_" + custom_disp_status

def get_disp_mode():
    global disp_status
    return disp_status

def get_bin_mode():
    global bin_status
    return bin_status

set_normal()
