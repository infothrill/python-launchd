# -*- coding: utf-8 -*-

import os
import plistlib


USER = 1
USER_ADMIN = 2
DAEMON_ADMIN = 3
USER_OS = 4
DAEMON_OS = 5

PLIST_LOCATIONS = {
    USER: '~/Library/LaunchAgents',  # Per-user agents provided by the user.
    USER_ADMIN: '/Library/LaunchAgents',  # Per-user agents provided by the administrator.
    DAEMON_ADMIN: '/Library/LaunchDaemons',  # System-wide daemons provided by the administrator.
    USER_OS: '/System/Library/LaunchAgents',  # Per-user agents provided by Mac OS X.
    DAEMON_OS: '/System/Library/LaunchDaemons',  # System-wide daemons provided by Mac OS X.
}


def compute_filename(label, scope):
    return os.path.expanduser(os.path.join(PLIST_LOCATIONS[scope], label + ".plist"))


def discover_filename(label, scope=None):
    if scope is not None:
        scopes = [scope]
    else:
        scopes = [k for k in PLIST_LOCATIONS]
    for thisscope in scopes:
        plistfilename = compute_filename(label, thisscope)
        if os.path.isfile(plistfilename):
            return plistfilename
    return None


def read(label, scope=None):
    with open(discover_filename(label, scope)) as f:
        return plistlib.readPlist(f)


def write(plist, label, scope):
    '''
    Writes the given property list to the appropriate file on disk and returns
    the absolute filename.

    :param plist: dict
    :param label: string
    :param scope: oneOf(USER, USER_ADMIN, DAEMON_ADMIN, USER_OS, DAEMON_OS)
    '''
    fname = compute_filename(label, scope)
    with open(fname, "wb") as f:
        plistlib.writePlist(plist, f)
    return fname
