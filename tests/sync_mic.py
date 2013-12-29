#!/usr/bin/env python

from sync_dist import sync_dist

if __name__ == '__main__':
    target = '/tmp/mic-0.22.3'
    dist_name = 'mic'
    dist_version = '0.22.3'

    status = sync_dist(target, dist_name, dist_version)

    print 'INFO: sync %s-%s in %s ...' % (dist_name, dist_version, target),
    if status:
        print 'OK'
    else:
        print 'FAIL'
