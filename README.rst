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


launchd is a pythonic wrapper around OS X's launchd command line tools. It
provides access to basic querying and interaction with launchd.

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
instantiating a LaunchdJob instance and querying the properties, which are
dynamically loaded:

.. code-block:: python

    finder = launchd.LaunchdJob("com.apple.Finder")
    finder.refresh()
    print(finder.pid)

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
