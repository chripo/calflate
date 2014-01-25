Welcome to Calflate
===================

Calflate is a tool to copy or import external calendar events 
into an online calendar.

It has no dependencies, it's open source and licenced under 
the *FreeBSD License*.

Developed @ https://github.com/chripo/calflate

Setup
-----

```sh
# create a virualenv
pip install https://github.com/chripo/calflate/zipball/master
ln -s $VIRTUAL_ENV/bin/calflate ~/bin/calflate
```

Insert and adjust the following section into a file, located at 
`~/.config/calflate.cfg`.

```sh
[COLLECTION-NAME]
verbose = true
src = https://srchost/usr/src_calendar.ics/
src_user = foofoo
src_pass = bar
dst = https://dsthost/usr/dst_calendar.ics/
dst_user = foo
dst_pass = bar
```
Execute `calflate --help` to show usage.
`calflate COLLECITON-NAME` to import a specific collection or 
`calflate *` to select all.

Contributions
-------------

Welcome!
