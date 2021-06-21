.. image:: https://img.shields.io/pypi/v/launchd.svg
    :target: https://pypi.python.org/pypi/launchd

.. image:: https://github.com/infothrill/python-launchd/actions/workflows/tests.yml/badge.svg?branch=main

*launchd* is a pythonic interface to interact with macOS's `launchd <https://en.wikipedia.org/wiki/Launchd>`_.
It provides access to basic querying and interaction with launchd. It is
implemented using the Objective C
`ServiceManagement framework <https://developer.apple.com/library/mac/documentation/General/Reference/ServiceManagementFwRef/_index.html#//apple_ref/doc/uid/TP40009335>`_
as well as the `launchd` command line utility. Therefore, this python package
can only be used on `macOS <http://en.wikipedia.org/wiki/MacOS>`_

The python objective C bridge contains some special types. This package strips
off all non built-in type information and returns pure python data.

Examples
========

The relevant import statement is:

.. code-block:: python

    import launchd


Listing all launchd jobs:

.. code-block:: python

    for job in launchd.jobs():
        print(job.label, job.pid, job.laststatus, job.properties, job.plistfilename)


Find the pid and laststatus of a job:

.. code-block:: python

   >>> launchd.LaunchdJob("com.apple.Finder").pid
   278

   >>> launchd.LaunchdJob("com.apple.Finder").laststatus
   0

   >>> launchd.LaunchdJob("com.example.fubar").pid
   Traceback (most recent call last):
     File "launchd/launchctl.py", line 78, in refresh
       raise ValueError("job '%s' does not exist" % self.label)
   ValueError: job 'com.example.fubar' does not exist

Detect if a job exists:

.. code-block:: python

   >>> launchd.LaunchdJob("com.example.fubar").exists()
   False

launchd job properties (these come directly from launchd and NOT the .plist files):

.. code-block:: python

   >>> launchd.LaunchdJob("com.apple.Finder").properties
   {'OnDemand': 1, 'PID': 278, 'PerJobMachServices': {'com.apple.coredrag': 0,
   'com.apple.axserver': 0, 'com.apple.CFPasteboardClient': 0,
   'com.apple.tsm.portname': 0}, 'LimitLoadToSessionType': 'Aqua',
   'Program': '/System/Library/CoreServices/Finder.app/Contents/MacOS/Finder',
   'TimeOut': 30, 'LastExitStatus': 0, 'Label': 'com.apple.Finder',
   'MachServices': {'com.apple.finder.ServiceProvider': 10}}

   >>> launchd.LaunchdJob("com.apple.Finder").properties["OnDemand"]
   1


Find all plist filenames of currently running jobs:

.. code-block:: python

   for job in launchd.jobs():
      if job.pid is None or job.plistfilename is None:
         continue
      print(job.plistfilename)

Job properties of a given job (this uses the actual .plist file):

.. code-block:: python

   >>> launchd.plist.read("com.apple.kextd")
   {'ProgramArguments': ['/usr/libexec/kextd'], 'KeepAlive': {'SuccessfulExit': False},
   'POSIXSpawnType': 'Interactive', 'MachServices': {'com.apple.KernelExtensionServer':
   {'HostSpecialPort': 15}}, 'Label': 'com.apple.kextd'}



Installation
============

.. code-block:: bash

    $ pip install launchd

or, if you want to work using the source tarball:

.. code-block:: bash

    $ python setup.py install


Requirements
============
* OS X >= 10.6
* Python 3.4+
