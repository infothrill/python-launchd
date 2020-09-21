# -*- coding: utf-8 -*-

import ServiceManagement

from .cmd import launchctl
from .plist import discover_filename
from .util import convert_NSDictionary_to_dict


class LaunchdJob(object):
    '''
    Custom class that allows us to lazily query the properties
    of the LaunchdJob when accessed.
    '''
    def __init__(self, label, pid=-1, laststatus=''):
        '''
        Instantiate a LaunchdJob instance. Only the label is required.
        If no pid or laststatus are specified, they will be queried when
        accessed.

        :param label: required string job label
        :param pid: optional int, if known. Can be None.
        :param laststatus: optional int, if known. Can be None.
        '''
        self._label = label
        if pid != -1:  # -1 indicates no value specified
            self._pid = pid
        if laststatus != '':
            self._laststatus = laststatus
        self._properties = None
        self._plist_fname = None

    @property
    def label(self):
        return self._label

    @property
    def pid(self):
        try:
            return self._pid
        except AttributeError:
            pass
        self.refresh()
        return self._pid

    @property
    def laststatus(self):
        try:
            return self._laststatus
        except AttributeError:
            self.refresh()
            return self._laststatus

    @property
    def properties(self):
        '''
        This is a lazily loaded dictionary containing the launchd runtime
        information of the job in question. Internally, this is retrieved
        using ServiceManagement.SMJobCopyDictionary(). Keep in mind that
        some dictionary keys are not always present (for example 'PID').
        If the job specified by the label cannot be found in launchd, then
        this method raises a ValueError exception.
        '''
        if hasattr(self, '_nsproperties'):
            self._properties = convert_NSDictionary_to_dict(self._nsproperties)
            del self._nsproperties
            # self._nsproperties = None
        if self._properties is None:
            self.refresh()
        return self._properties

    def exists(self):
        return ServiceManagement.SMJobCopyDictionary(None, self.label) is not None

    def refresh(self):
        val = ServiceManagement.SMJobCopyDictionary(None, self.label)
        if val is None:
            raise ValueError("job '%s' does not exist" % self.label)
        else:
            self._properties = convert_NSDictionary_to_dict(val)
            # update pid and laststatus attributes
            try:
                self._pid = self._properties['PID']
            except KeyError:
                self._pid = None
            try:
                self._laststatus = self._properties['LastExitStatus']
            except KeyError:
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


def jobs():
    for entry in ServiceManagement.SMCopyAllJobDictionaries(None):
        label = entry['Label']
        if label.startswith("0x"):
            continue
        try:
            pid = int(entry['PID'])
        except KeyError:
            pid = None
        try:
            laststatus = int(entry['LastExitStatus'])
        except KeyError:
            laststatus = None
        job = LaunchdJob(label, pid, laststatus)
        job._nsproperties = entry
        yield job


def load(*args):
    return launchctl("load", *args)


def unload(*args):
    return launchctl("unload", *args)
