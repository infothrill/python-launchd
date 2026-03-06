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
        print(job.label, job.pid, job.properties, job.plistfilename)


Find the pid of a job:

.. code-block:: python

   >>> launchd.LaunchdJob("com.apple.Finder").pid
   278

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
   {'Label': 'com.apple.Finder', 'PlistPath': '/System/Library/LaunchAgents/com.apple.Finder.plist', 'Scope': 4, 'Status': 'unknown', 'StatusCode': None, 'Registered': True}

   >>> launchd.LaunchdJob("com.apple.Finder").properties["Label"]
   'com.apple.Finder'


Find all plist filenames of currently running jobs:

.. code-block:: python

   for job in launchd.jobs():
      if job.pid is None or job.plistfilename is None:
         continue
      print(job.plistfilename)

Job properties of a given job (this uses the actual .plist file):

.. code-block:: python

   >>> launchd.plist.read("com.apple.Finder")
   {'POSIXSpawnType': 'App', 'RunAtLoad': False, 'KeepAlive': {'SuccessfulExit': False, 'AfterInitialDemand': True}, 'Label': 'com.apple.Finder', 'Program': '/System/Library/CoreServices/Finder.app/Contents/MacOS/Finder', 'CFBundleIdentifier': 'com.apple.finder', 'ThrottleInterval': 1}



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
* Python 3.10+
* macOS 13+ for the SMAppService-backed job metadata API

SMAppService integration
=======================

Job metadata is now collected through Apple’s `SMAppService <https://developer.apple.com/documentation/servicemanagement/smappservice>`_ API. Because that interface only exposes helper plists that the calling bundle can manage, `launchd.jobs()` now reports the property lists SMAppService can inspect (status, bundled configuration, etc.). `pid`/`LastExitStatus` therefore remain ``None`` in most cases, but ``properties["Config"]`` still contains the original plist contents. The low-level `launchctl` binary remains the implementation for ``load()``/``unload()`` until Apple publishes a direct replacement.
