python-launchd - pythonic interface for launchd
================================================

.. image:: https://travis-ci.org/infothrill/python-launchd.png
    :target: https://travis-ci.org/infothrill/python-launchd

.. image:: https://coveralls.io/repos/infothrill/python-launchd/badge.png
        :target: https://coveralls.io/r/infothrill/python-launchd

.. image:: https://badge.fury.io/py/launchd.png
    :target: http://badge.fury.io/py/launchd

.. image:: https://pypip.in/d/launchd/badge.png
        :target: https://crate.io/packages/launchd/


launchd is a pythonic interface to interact with OS X's `launchd <https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man8/launchd.8.html>`_. It provides
access to basic querying and interaction with launchd by using the Objective C 
`ServiceManagement framework <https://developer.apple.com/library/mac/documentation/General/Reference/ServiceManagementFwRef/_index.html#//apple_ref/doc/uid/TP40009335>`_
as well as the `launchd` command line utility.


Examples
========

The relevant import statement is:

.. code-block:: python

    import launchd


Listing all launchd jobs:

.. code-block:: python

    for job in launchd.jobs():
        print(job.label, job.pid, job.status, job.properties, job.plistfilename)


Detecting launchd runtime properties based on a label works by manually
instantiating a LaunchdJob instance and loading its properties, either by
specifying 'load' in the constructor or calling .refresh():

.. code-block:: python

    finder = launchd.LaunchdJob("com.apple.Finder", load=True)
    print(finder.pid)

    fubar = launchd.LaunchdJob("com.apple.Fubar")
    if fubar.exists():
        fubar.refresh()
    else:
        print("No such launchd job: %s" % fubar.label)

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
* Python 2.7, 3.2 or 3.3
