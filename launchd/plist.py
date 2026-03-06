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


def compute_directory(scope: int) -> str:
    return os.path.expanduser(PLIST_LOCATIONS[scope])


def compute_filename(label: str, scope: int) -> str:
    return os.path.join(compute_directory(scope), label + ".plist")


def discover_filename(label: str, scopes: None | int | tuple[int] | list[int] = None) -> str | None:
    """
    Check the filesystem for the existence of a .plist file matching the job label.
    Optionally specify one or more scopes to search (default all).

    :param label: string
    :param scope: tuple or list or oneOf(USER, USER_ADMIN, DAEMON_ADMIN, USER_OS, DAEMON_OS)
    """
    if scopes is None:
        scopes = list(PLIST_LOCATIONS)
    elif not isinstance(scopes, (list, tuple)):
        scopes = (scopes, )
    for thisscope in scopes:
        plistfilename = compute_filename(label, thisscope)
        if os.path.isfile(plistfilename):
            return plistfilename
    return None


def read(label: str, scope: int | None = None):
    fname = discover_filename(label, scope)
    if fname is not None:
        with open(fname, "rb") as f:
            return plistlib.load(f)
    else:
        raise ValueError(f"No plist file found for label {label} and scope {scope}!")


def write(label: str, plist, scope=USER) -> str:
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
