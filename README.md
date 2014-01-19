Welcome to Calflate
===================

Calflate is a tool to copy or import external calendar events 
into an online calendar.

It has no dependencies, it's open source and licenced under 
the *FreeBSD License*.

Developed @ https://github.com/chripo/calflate

Setup
-----

### Fire And Forget Approach

```sh
curl https://raw2.github.com/chripo/calflate/master/calflate/__init__.py -o ~/bin/calflate_foo

chmod u+x ~/bin/calflate_foo

$EDITOR ~/bin/calflate_foo

# add as first line
#!/usr/bin/env python

# add as third line and adjust
SRC = ('https://calendar,source.com/foo.ics/', 'test', 'test')
DST = ('https://my.radicale.org/test/test.ics/', 'test', 'test')
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
