# sync-dist #


## what's sync-dist ##

`sync-dist` copys all files belong to a python distribution installed in host
into a directory. It's useful, if you want to pack a python distribution and
deploy it to another enviroment.


## how to use ##

A distribution consists of purelib, platlib, headers, scripts and data. If
you want `sync-dist` to collect all distribuiton files, you MUST create a
metadata file `[dist-name]-[dist-version]` in `sync_dist/meta` for the
specified distribution. The following is the metadata file for `pip-1.3.1`:

```
dist_name = 'pip'
dist_version = '1.3.1'
purelib = ['pip']
scripts = ['pip', 'pip-python', 'python-pip']
data = ['/usr/share/doc/python-pip-1.3.1']
```

After this, you can call `sync_dist` function in a python file. By default,
this function search  distribution files with the following variables. If
the specified distribute has different configurations as the default ones,
please provide them to this functions.

```
root        = '/'
home        = '~'
prefix      = sys.prefix
exec_prefix = sys.prefix
py_version  = sys.version.split()[0]
```

What a pity! If the distribution was installed with customized paths,
`sync-dist` will need more help to work. You MUST provide these paths
as the following names:

```
purelib_path
platlib_path
headers_path
scripts_path
data_path
```


## license ##


## author ##

Written by Myth
