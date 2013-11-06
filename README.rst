python-launchd - pythonic interface for launchd
===============================================

.. image:: https://badge.fury.io/py/launchd.png
    :target: http://badge.fury.io/py/launchd

.. image:: https://pypip.in/d/launchd/badge.png
        :target: https://crate.io/packages/launchd/


launchd is a pythonic interface to interact with OS X's `launchd <https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man8/launchd.8.html>`_.
It provides access to basic querying and interaction with launchd. It is
implemented using the Objective C 
`ServiceManagement framework <https://developer.apple.com/library/mac/documentation/General/Reference/ServiceManagementFwRef/_index.html#//apple_ref/doc/uid/TP40009335>`_
as well as the `launchd` command line utility. Therefore, this python package
can only be used on `OS X <http://en.wikipedia.org/wiki/OS_X>`_

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
        print(job.label, job.pid, job.status, job.properties, job.plistfilename)


To query existing job properties, instantiate a LaunchdJob instance with a label
and query its pid, lastatus and properties:

.. code-block:: python

    # PID of Finder
    print(launchd.LaunchdJob("com.apple.Finder").pid)

    # Detecting if a job is defined
    if launchd.LaunchdJob("com.apple.Fubar").exists():
        print("OK")
    else:
        print("No such launchd job: %s" % fubar.label)

    # arbitrary launchd property querying:
    print(launchd.LaunchdJob("com.apple.Finder").properties["OnDemand"])


Find all plist filenames of currently running jobs:

.. code-block:: python

    for job in launchd.jobs():
        if job.pid is None or job.plistfilename is None:
            continue
        print(job.plistfilename)


Installation
============

.. code-block:: bash

    # NOT YET AVAILABLE
    $ pip install launchd

or, if you want to work using the source tarball:

.. code-block:: bash

    $ python setup.py install
  

Requirements
============
* OS X >= 10.6
* Python 2.7, 3.2 or 3.3
