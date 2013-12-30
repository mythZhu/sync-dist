#!/usr/bin/env python

import os
import sys

from distutils.util import subst_vars
from distutils.command.install import INSTALL_SCHEMES, SCHEME_KEYS

from meta import DIST_META_KEYS, import_dist_meta, get_py_version
from errors import LocationError, MetadataError


__all__ = [
    'FREEZE_SCHEME',
    'SCHEME_KEYS',
    'walk_tree',
    'locate_distribution',
    'freeze_distribution',
    'locate_dist_section',
    'freeze_dist_section',
    ]


def _gen_freeze_scheme():
    """ Generate scheme to freeze distribution.
    """
    freeze_scheme = {}

    for key in SCHEME_KEYS:
        paths = []
        for scheme_name, install_scheme in INSTALL_SCHEMES.iteritems():
            val = install_scheme[key]
            if scheme_name == 'unix_home':
                val = val.replace('$base', '$home', 1)
            else:
                val = val.replace('$base', '$prefix', 1)
                val = val.replace('$platbase', '$exec_prefix', 1)
            paths.append(val)
        freeze_scheme[key] = paths

    return freeze_scheme


FREEZE_SCHEME = _gen_freeze_scheme()


def walk_tree(top):
    """ List the whole directory tree down from the top.
    """
    nodes = [top]
    for dirpath, dirnames, filenames in os.walk(top):
        for dirname in dirnames:
            nodes.append(os.path.join(dirpath, dirname))
        for filename in filenames:
            nodes.append(os.path.join(dirpath, filename))

    return nodes


def _expand_prefix(prefix, configs):
    """ Expand variables in the prefix.
    """
    return subst_vars(prefix, configs)


def _verify_prefix(prefix, files):
    """ Verify that every file exists with the specified prefix.
    """
    for f in files:
        f = os.path.join(prefix, f)
        if not os.path.exists(f):
            return False
    else:
        return True


def locate_dist_section(section, dist_meta):
    """ Find and return the location of the specified section.
    """
    def purelib_path_gen():
        paths = FREEZE_SCHEME['purelib']
        paths.extend(sys.path)
        return paths

    def platlib_path_gen():
        # TODO: more available paths
        paths = FREEZE_SCHEME['platlib']
        return paths

    def headers_path_gen():
        # TODO: more available paths
        paths = FREEZE_SCHEME['headers']
        return paths

    def scripts_path_gen():
        paths = FREEZE_SCHEME['scripts']
        if os.environ.has_key('PATH'):
            paths.extend(os.environ['PATH'].split(":"))
        if os.environ.has_key('HOME'):
            paths.append(os.path.join(os.environ['HOME'], 'bin'))
        return paths

    def data_path_gen():
        # TODO: more available paths
        paths = FREEZE_SCHEME['data']
        return paths


    if section not in SCHEME_KEYS:
        raise LocationError("illegal section name '%s'." % section)

    pathvar = dist_meta.get('%s_path' % section, None)
    if pathvar:
        paths = [pathvar]
    else:
        pathgen = locals()['%s_path_gen' % section]
        paths = pathgen()

    for prefix in paths:
        prefix = _expand_prefix(prefix, dist_meta)
        status = _verify_prefix(prefix, dist_meta[section])
        if status:
            return prefix
    else:
        raise LocationError("cann't locate section '%s'." % section)


def freeze_dist_section(section, dist_meta):
    """ List all files belong to the specified section.
    """
    location = locate_dist_section(section, dist_meta)

    outfiles = []
    for f in dist_meta.get(section, []):
        f = os.path.join(location, f)
        if f not in outfiles:
            outfiles.extend(walk_tree(f))

    return location, outfiles


def freeze_distribution(dist_name, dist_version, **attrs):
    """ List all files belong to the specified distribution.
    """
    for key in attrs.iterkeys():
        if key not in DIST_META_KEYS:
            raise AttributeError("unexpected keyword argument '%s'." % key)

    try:
        dist_meta = import_dist_meta(dist_name, dist_version)
        dist_meta.update(attrs)
    except ImportError:
        raise MetadataError("metadata of '%s-%s' not found." % \
                            (dist_name, dist_version))

    dist_files = []
    dist_scheme = {}

    for key in SCHEME_KEYS:
        location, outfiles = freeze_dist_section(key, dist_meta)
        dist_files.extend(outfiles)
        dist_scheme[key] = location

    return dist_scheme, dist_files
