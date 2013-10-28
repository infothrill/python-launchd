# -*- coding: utf-8 -*-

import sys
import plistlib

from .cmd import launchctl
from .plist import discover_filename


class LaunchdJob(object):
    '''
    Custom class that allows us to lazily load the properties
    of the LaunchdJob when accessed.
    '''
    def __init__(self, label, pid=None, laststatus=None):
        self._label = label
        self._pid = pid
        self._laststatus = laststatus
        self._properties = None
        self._plist_fname = None

    def _reset(self):
        self._pid = None
        self._laststatus = None
        self._properties = None
        self._plist_fname = None

    @property
    def label(self):
        return self._label

    @property
    def pid(self):
        return self._pid

    @property
    def laststatus(self):
        return self._laststatus

    @property
    def properties(self):
        '''
        This is a lazily loaded dictionary containing the launchd runtime
        information of the job in question. Internally, this is retrieved
        using `launchctl -x LABEL`. Keep in mind that some dictionary keys
        are not always present (for example 'PID').
        '''
        if self._properties is None:
            self.refresh()
        return self._properties

    def refresh(self):
        from subprocess import CalledProcessError
        try:
            self._properties = job_properties(self)
        except CalledProcessError:
            self._reset()
            raise ValueError("This job ('%s') does not exist" % str(self.label))
        else:
            # update pid and laststatus attributes
            if 'PID' in self._properties:
                self._pid = self._properties['PID']
            else:
                self._pid = None
            if 'LastExitStatus' in self._properties:
                self._laststatus = self._properties['LastExitStatus']
            else:
                self._laststatus = None

    @property
    def plistfilename(self):
        '''
        This is a lazily detected absolute filename of the corresponding
        property list file (*.plist). None if it doesn't exist.
        '''
        if self._plist_fname is None:
            self._plist_fname = discover_filename(self.label)
        return self._plist_fname


def job_properties(job):
    '''
    Wrapper for `launchctl -x LABEL`

    Returns dictionary
    :param job: string label or LaunchdJob
    '''
    if isinstance(job, LaunchdJob):
        str_label = job.label
    else:
        str_label = job
    if sys.version_info < (3, 0):
        return dict(plistlib.readPlistFromString(launchctl("list", "-x", str_label)))
    else:
        return dict(plistlib.readPlistFromBytes(launchctl("list", "-x", str_label)))


def jobs():
    '''
    Wrapper for `launchctl list`

    Returns a generator for LaunchdJob
    '''
    if sys.version_info < (3, 0):
        stdout = launchctl("list")
    else:
        stdout = launchctl("list").decode("utf-8")
    # PID, Status, Label
    lines = iter(stdout.splitlines())
    # skip first line
    next(lines)
    sep = "\t"
    Ox = "0x"
    for line in lines:
        pid, _, last = line.strip().partition(sep)
        status, _, label = last.strip().partition(sep)
        if label.startswith(Ox):
            continue
        if pid.isdigit():
            pid = int(pid)
        else:
            pid = None
        if status.isdigit():
            status = int(status)
        else:
            status = None
        yield LaunchdJob(label, pid, status)


def start():
    pass


def stop():
    pass


def load(*args):
    return launchctl("load", *args)


def unload(*args):
    return launchctl("unload", *args)
