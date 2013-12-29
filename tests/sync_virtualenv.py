#!/usr/bin/env python

from sync_dist import sync_dist

if __name__ == '__main__':
    target = '/tmp/virtual-1.10.1'
    dist_name = 'virtualenv'
    dist_version = '1.10.1'

    status = sync_dist(target, dist_name, dist_version)

    print 'INFO: sync %s-%s in %s ...' % (dist_name, dist_version, target),
    if status:
        print 'OK'
    else:
        print 'FAIL'
