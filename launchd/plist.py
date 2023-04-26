# -*- coding: utf-8 -*-

import os
import plistlib

USER = 1
USER_ADMIN = 2
DAEMON_ADMIN = 3
USER_OS = 4
DAEMON_OS = 5

PLIST_LOCATIONS = {
    USER: "~/Library/LaunchAgents",  # Per-user agents provided by the user.
    USER_ADMIN: "/Library/LaunchAgents",  # Per-user agents provided by the administrator.
    DAEMON_ADMIN: "/Library/LaunchDaemons",  # System-wide daemons provided by the administrator.
    USER_OS: "/System/Library/LaunchAgents",  # Per-user agents provided by Mac OS X.
    DAEMON_OS: "/System/Library/LaunchDaemons",  # System-wide daemons provided by Mac OS X.
}


def compute_directory(scope):
    return os.path.expanduser(PLIST_LOCATIONS[scope])


def compute_filename(label, scope):
    return os.path.join(compute_directory(scope), label + ".plist")


def discover_filename(label: str, scopes=None) -> str:
    """
    Check the filesystem for the existence of a .plist file matching the job label.
    Optionally specify one or more scopes to search (default all).

    :param label: string
    :param scope: tuple or list or oneOf(USER, USER_ADMIN, DAEMON_ADMIN, USER_OS, DAEMON_OS)
    """
    scopes = scopes or tuple(PLIST_LOCATIONS)
    if not isinstance(scopes, (list, tuple)):
        scopes = (scopes, )
    for thisscope in scopes:
        plistfilename = compute_filename(label, thisscope)
        if os.path.isfile(plistfilename):
            return plistfilename
    raise FileNotFoundError(f"{label}, {scopes}")


def read(label, scope=None):
    with open(discover_filename(label, scope), "rb") as f:
        return plistlib.load(f)


def write(label, plist, scope=USER):
    """
    Write the property list to file on disk and return filename.

    Creates the underlying parent directory structure if missing.
    :param plist: dict
    :param label: string
    :param scope: oneOf(USER, USER_ADMIN, DAEMON_ADMIN, USER_OS, DAEMON_OS)
    """
    os.makedirs(compute_directory(scope), mode=0o755, exist_ok=True)
    fname = compute_filename(label, scope)
    with open(fname, "wb") as f:
        plistlib.dump(plist, f)
    return fname
