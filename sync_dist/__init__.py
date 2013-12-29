#!/usr/bin/env python

import os
import shutil
from distutils.util import change_root

from freeze import freeze_distribution
from errors import DistributionError


__all__ = ['remove_file_or_dir', 'copy_file_or_dir', 'sync_dist']


def remove_file_or_dir(file_or_dir):
    """ Remove a file node whatever its type.
    """
    if not os.path.exists(file_or_dir):
        return True

    if os.path.isdir(file_or_dir):
        shutil.rmtree(file_or_dir)
    else:
        os.unlink(file_or_dir)

    return os.path.exists(file_or_dir)


def copy_file_or_dir(file_or_dir, dest_path, force=False):
    """ Copy a file node whatever its type.
    """
    if os.path.exists(dest_path):
        if force:
            remove_file_or_dir(dest_path)
        else:
            return False

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    if os.path.isdir(file_or_dir):
        shutil.copytree(file_or_dir, dest_path)
    else:
        shutil.copyfile(file_or_dir, dest_path)

    return os.path.exists(dest_path)


def sync_dist(target, dist_name, dist_version, **dist_attrs):
    """ Copy all files of a distribution installed in host into a directory.

        A distribution consists of purelib, platlib, headers, scripts
        and data. By default, this function resolves their paths with
        the following variables:

            root        = '/'
            home        = '~'
            prefix      = sys.prefix
            exec_prefix = sys.prefix
            py_version  = sys.version.split()[0]

        If the specified distribute has different configurations as
        the default ones, please provide them to this functions.

        If the specified distribute was installed with customized paths,
        please provide them as the following names:

            purelib_path
            platlib_path
            headers_path
            scripts_path
            data_path
    """
    try:
        dist_scheme, dist_files = \
            freeze_distribution(dist_name, dist_version, **dist_attrs)
    except DistributionError, err:
        return False

    if not os.path.exists(target):
        os.makedirs(target)

    for dist_file in filter(os.path.isfile, dist_files):
        copy_file = change_root(target, dist_file)
        copy_file_or_dir(dist_file, copy_file, force=True)

    # -- DEBUG ---------------------------------------------------
    # for nu, df in enumerate(sorted(dist_files), 1): print nu, df

    return True
