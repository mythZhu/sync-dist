#!/usr/bin/env python

dist_name = 'mic'

dist_version = '0.22.3'

py_version = '2.7'

purelib = [
    'mic',
    'mic/utils',
    'mic/imager',
    'mic/kickstart',
    'mic/kickstart/custom_commands',
    'mic/3rdparty/pykickstart',
    'mic/3rdparty/pykickstart/commands',
    'mic/3rdparty/pykickstart/handlers',
    'mic/3rdparty/pykickstart/urlgrabber',
    ]

scripts = [
    'mic',
    ]

data = [
    '/etc/mic',
    '/etc/bash_completion.d/mic.sh',
    '/etc/zsh_completion.d/_mic',
    '/usr/lib/mic/plugins/imager',
    '/usr/lib/mic/plugins/backend',
    '/usr/share/doc/mic-0.22.3',
    '/usr/share/man/man1/mic.1.gz'
    ]
