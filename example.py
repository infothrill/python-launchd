# -*- coding: utf-8 -*-
"""
Example script showing how to install and remove plist based launchd jobs.
"""

import sys
import os

import launchd


def install(label, plist):
    """
    Store a new .plist file and load it.

    :param label: job label
    :param plist: a property list dictionary
    """
    fname = launchd.plist.write(label, plist)
    launchd.load(fname)


def uninstall(label):
    """
    Remove a .plist file and unload it.

    :param label: job label
    """
    if launchd.LaunchdJob(label).exists():
        fname = launchd.plist.discover_filename(label)
        launchd.unload(fname)
        os.unlink(fname)


def main():
    myplist = {
        "Disabled": False,
        "Label": "testlaunchdwrapper_python",
        "Nice": -15,
        "OnDemand": True,
        "ProgramArguments": ["/bin/bash", "-c", "sleep 1 && echo 'Hello World' && exit 0"],
        "RunAtLoad": True,
        "ServiceDescription": "runs a sample command",
        "ServiceIPC": False,
    }

    import time
    label = myplist["Label"]
    job = launchd.LaunchdJob(label)
    if not job.exists():
        print("'%s' is not loaded in launchd. Installing..." % (label))  # noqa: T001
        install(label, myplist)
        while job.pid is not None:
            print("Alive! PID = %s" % job.pid)  # noqa: T001
            job.refresh()
            time.sleep(0.2)
    else:
        if job.pid is None:
            print("'%s' is loaded but not currently running" % (job.label))  # noqa: T001
        else:
            print("'%s' is loaded and currently running: PID = %s" % (job.label, job.pid))  # noqa: T001
            while job.pid is not None:
                print("Alive! PID = %s" % job.pid)  # noqa: T001
                job.refresh()
                time.sleep(0.2)

    print("Uninstalling again...")  # noqa: T001
    uninstall(label)
    return 0


if __name__ == "__main__":
    sys.exit(main())
