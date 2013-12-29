#!/usr/bin/env python

import os

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


def _get_egg_name(dist_name, dist_version):
    """ Return the name of egg information file.
    """
    return "%s-%s-py%s.egg-info" % \
           (dist_name, dist_version, get_py_version()[:3])


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


def locate_dist_section(section, dist_meta, **attrs):
    """ Find and return the location of the specified section.
    """
    if section not in SCHEME_KEYS:
        raise LocationError("illegal section name '%s'." % section)

    pathvar = dist_meta['%s_path' % section]
    pathgen = attrs.get('%s_path_gen' % section, None)

    if pathvar:
        paths = [pathvar]
    elif pathgen:
        paths = pathgen()
    else:
        paths = FREEZE_SCHEME[section]

    for prefix in paths:
        prefix = _expand_prefix(prefix, dist_meta)
        status = _verify_prefix(prefix, dist_meta[section])
        if status:
            return prefix
    else:
        raise LocationError("cann't locate section '%s'." % section)


def freeze_dist_section(section, dist_meta, **attrs):
    """ List all files belong to the specified section.
    """
    location = locate_dist_section(section, dist_meta, **attrs)

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

    egg_name = _get_egg_name(dist_name, dist_version)
    egg_path = os.path.join(dist_scheme['purelib'], egg_name)
    dist_files.extend(walk_tree(egg_path))

    return dist_scheme, dist_files
