# -*- coding: utf-8 -*-

import sys
import os

import launchd

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


def install():
    fname = launchd.plist.write(myplist, myplist['Label'], launchd.plist.USER)
    launchd.load(fname)


def uninstall():
    fname = launchd.plist.discover_filename(myplist['Label'])
    job = launchd.LaunchdJob(myplist['Label'])
    try:
        job.refresh()
    except ValueError:
        pass
    else:
        launchd.unload(fname)
        os.unlink(fname)


def main():
    import time
    job = launchd.LaunchdJob(myplist['Label'])
    try:
        job.refresh()
    except ValueError:
        print("'%s' is not loaded in launchd. Installing..." % (job.label))
        install()
        job.refresh()
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
    uninstall()
    return 0


if __name__ == '__main__':
    sys.exit(main())
