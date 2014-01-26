Welcome to Calflate
===================

*Calflate* is a command line application that **conflates** external 
*CalDAV* and *CardDAV* entries into an other online collection. 
It does an one-way sync of calendar EVENTs, TODOs, JOURNALs and 
addressbook entries (VCARD) based on ``UIDs`` and ``SEQUENCE`` or 
``REV`` numbers.

*Calflate* is written in Python, it has no dependencies and 
licenced under the **FreeBSD License**. The source code and 
issue tracker is available at https://github.com/chripo/calflate.

Featues
-------

+ one-way sync of VEVENT, VTODO, VJOURNAL and VCARD
+ rewrite / cleanup UIDs based on regular expressions
+ import entries from local files and online collections
+ is able to purge destination items
+ supports multiple collection sets
+ configurable per collection

Quickstart
----------

**Install from source**

::

    # create a virualenv
    pip install https://github.com/chripo/calflate/zipball/master
    ln -s $VIRTUAL_ENV/bin/calflate ~/bin/calflate

**Configure**

Create a configuration file  at ``~/.config/calflate.cfg``. Insert 
the following section for each collection that should be imported.

::

    [COLLECTION-NAME]
    # ignore input argument from command line
    # input = None
    
    # never purge destination items
    # purge = False
    
    # verbose output
    # verbose = True
    
    # don't make changes
    # dryrun = True
    
    # replace UID pattern
    # uid_from = (.+?)@foobar.com
    # uid_to = \1
    
    # source calendar / addressbook
    src = https://source-host.net/test/events.ics/
    # src_user = username
    # src_pass = password
    
    # destination calendar / addressbook
    dst = https://my-server.net/user/calendar.ics/
    dst_user = username
    dst_pass = password


**Execute**

- ``calflate --help`` to show usage. 
- ``calflate COLLECTION-NAME`` to import a specific collection or 
- ``calflate '*'`` to conflate all sets.

Contributions
-------------

Are welcome! Resepect PEP-8.

