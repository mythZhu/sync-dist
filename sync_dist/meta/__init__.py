#!/usr/bin/env python

import os
import sys
import site
from imp import find_module, load_module


__all__ = [
    'DIST_META_KEYS',
    'get_py_version',
    'get_home_path',
    'import_dist_meta',
    ]


DIST_META_KEYS = (
    # base
    'dist_name',
    'dist_version',
    'py_version',
    'purelib',
    'platlib',
    'headers',
    'scripts',
    'data',
    # path
    'root',
    'home',
    'prefix',
    'exec_prefix',
    'userbase',
    'usersite',
    'purelib_path',
    'platlib_path',
    'headers_path',
    'scripts_path',
    'data_path',
    )


def get_py_version():
    """ Return the version of current python interpreter.
    """
    return sys.version.split()[0]


def get_home_path():
    """ Return the path of current user's home directory.
    """
    return os.path.expanduser('~')


def _get_default_meta():
    """ Return a canonical metadata with default values.
    """
    meta = {
        'dist_name'   : 'UNKNOWN',
        'dist_version': '0.0.0',
        'py_version'  : get_py_version(),
        'purelib'     : [],
        'platlib'     : [],
        'headers'     : [],
        'scripts'     : [],
        'data'        : [],
        'root'        : os.path.normpath('/'),
        'home'        : get_home_path(),
        'prefix'      : os.path.normpath(sys.prefix),
        'exec_prefix' : os.path.normpath(sys.exec_prefix),
        'userbase'    : site.USER_BASE,
        'usersite'    : site.USER_SITE,
        'purelib_path': None,
        'platlib_path': None,
        'headers_path': None,
        'scripts_path': None,
        'data_path'   : None,
        }

    py_version = meta['py_version']
    meta['py_version_short'] = py_version[:3]
    meta['py_version_nodot'] = py_version[0] + py_version[2]

    return meta


def import_dist_meta(name, version):
    """ Load and return distribution metadata.
    """
    try:
        fullname = '%s-%s' % (name, version)
        mod = load_module(name, *find_module(fullname, __path__))
    except ImportError:
        return None

    dist_meta = _get_default_meta()

    for key in DIST_META_KEYS:
        try:
            dist_meta[key] = getattr(mod, key)
        except AttributeError:
            pass

    return dist_meta
