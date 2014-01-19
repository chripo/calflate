Welcome to Calflate
===================

Calflate is a simple script to copy or import external
calendar events into an online calendar.

It has no dependencies, it's Open Source Software and
licenced under a *FreeBSD License*.

Developed @ https://github.com/chripo/calflate

Setup
-----

### Fire And Forget Approach

```sh
curl https://raw2.github.com/chripo/calflate/master/calflate/__init__.py -o ~/bin/calflate_foo

chmod u+x ~/bin/calflate_foo

$EDITOR ~/bin/calflate_foo

# as first line add
#!/usr/bin/env python

# as third line add and adjust
SRC=('https://calendar,source.com/foo.ics/', 'test', 'test')
DST=('https://my.radicale.org/test/test.ics/', 'test', 'test')
```

save, exit and run with argument --dry-run first

### Maintainable Strategy

```sh
git clone https://github.com/chripo/calflate.git
cd calflate
git checkout -t -b local
cp mycalflate.py calflate_foo.py
edit SRC and DST in calflate_foo.py
run and commit to local branch
```

Contributions
-------------

Welcome!
