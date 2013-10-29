# -*- coding: utf-8 -*-

import ServiceManagement

from .cmd import launchctl
from .plist import discover_filename


class LaunchdJob(object):
    '''
    Custom class that allows us to lazily load the properties
    of the LaunchdJob when accessed.
    '''
    def __init__(self, label, pid=None, laststatus=None, load=False):
        '''
        Instantiate a LaunchdJob instance. Only the label is truly required.
        If no pid or laststatus are specified, they will be detected during
        construction.

        :param label: required string job label
        :param pid: optional int, if known. Can be None.
        :param laststatus: optional int, if known. Can be None.
        :param load: boolean. Load job details from launchd during construction.
        '''
        self._label = label
        if load:
            self.refresh()
        else:
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
        If the job specified by the label cannot be found in launchd, then
        this method raises a ValueError exception.
        '''
        if self._properties is None:
            self.refresh()
        return self._properties

    def exists(self):
        from subprocess import CalledProcessError
        try:
            _ = job_properties(self.label)
        except (CalledProcessError, ValueError):
            return False
        else:
            return True

    def refresh(self):
        from subprocess import CalledProcessError
        try:
            self._properties = job_properties(self.label)
        except (CalledProcessError, ValueError):
            self._reset()
            raise ValueError("The job ('%s') does not exist!" % self.label)
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


def job_properties(joblabel):
    val = ServiceManagement.SMJobCopyDictionary(None, joblabel)
    if val is None:
        raise ValueError("job %s does not exist" % joblabel)
    return dict(val)


def jobs():
    for entry in ServiceManagement.SMCopyAllJobDictionaries(None):
        if entry['Label'].startswith("0x"):
            continue
        label = entry['Label']
        if 'PID' in entry:
            pid = int(entry['PID'])
        else:
            pid = None
        if 'LastExitStatus' in entry:
            status = int(entry['LastExitStatus'])
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
