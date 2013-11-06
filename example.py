# -*- coding: utf-8 -*-
"""
Example script showing how to install and remove plist based launchd jobs
"""

import sys
import os

import launchd


def install(label, plist):
    '''
    Utility function to store a new .plist file and load it

    :param label: job label
    :param plist: a property list dictionary
    '''
    fname = launchd.plist.write(label, plist)
    launchd.load(fname)


def uninstall(label):
    '''
    Utility function to remove a .plist file and unload it

    :param label: job label
    '''
    if launchd.LaunchdJob(label).exists():
        fname = launchd.plist.discover_filename(label)
        launchd.unload(fname)
        os.unlink(fname)


def main():
    myplist = dict(
              Disabled=False,
              Label="testlaunchdwrapper_python",
              Nice=-15,
              OnDemand=True,
              ProgramArguments=["/bin/bash", "-c", "sleep 1 && echo 'Hello World' && exit 0"],
              RunAtLoad=True,
              ServiceDescription="runs a sample command",
              ServiceIPC=False,
              )

    import time
    label = myplist['Label']
    job = launchd.LaunchdJob(label)
    if not job.exists():
        print("'%s' is not loaded in launchd. Installing..." % (label))
        install(label, myplist)
        while job.pid is not None:
            print("Alive! PID = %s" % job.pid)
            job.refresh()
            time.sleep(0.2)
    else:
        if job.pid is None:
            print("'%s' is loaded but not currently running" % (job.label))
        else:
            print("'%s' is loaded and currently running: PID = %s" % (job.label, job.pid))
            while job.pid is not None:
                print("Alive! PID = %s" % job.pid)
                job.refresh()
                time.sleep(0.2)

    print("Uninstalling again...")
    uninstall(label)
    return 0


if __name__ == '__main__':
    sys.exit(main())
