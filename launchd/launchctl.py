from .cmd import launchctl
from .service import ServiceStatus, enumerate_services, get_service_info
from .plist import discover_filename


class LaunchdJob:
    """
    Class to lazily query the properties of the LaunchdJob when accessed.
    """

    def __init__(self, label: str, pid: int = -1):
        """
        Instantiate a LaunchdJob instance. Only the label is required.
        If no pid is specified, it will be queried when accessed.

        :param label: required string job label
        :param pid: optional int, if known. Can be None.
        """
        self._label = label
        if pid != -1:  # -1 indicates no value specified
            self._pid = pid
        self._properties = {}
        self._plist_fname = None

    def __repr__(self) -> str:
        """Represent instance as string."""
        return f"LaunchdJob(label={self._label})"

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
        """Unsupported since 1.0.0."""
        raise AttributeError("This property is not supported since 1.0.0")

    @property
    def properties(self) -> dict:
        """
        Lazily load dictionary with launchd runtime information.

        Internally, this is retrieved using ServiceManagement.SMAppService helpers.
        Keep in mind that some dictionary keys are not always present (for example 'PID').
        If the job specified by the label cannot be found in launchd, then
        this method raises a ValueError exception.
        """
        if self._properties == {}:
            self.refresh()
        return self._properties

    def exists(self):
        info = get_service_info(self.label)
        return info is not None and info.status != ServiceStatus.NOT_FOUND

    def refresh(self):
        info = get_service_info(self.label)
        if info is None:
            raise ValueError("job '%s' does not exist" % self.label)
        self._properties = info.properties
        from AppKit import NSRunningApplication

        def get_pid_by_bundle_id(bundle_id):
            # Retrieve all running applications with the specific bundle identifier
            apps = NSRunningApplication.runningApplicationsWithBundleIdentifier_(bundle_id.lower())
            if not apps:
                return None
            # In most cases, there is only one instance (like Finder)
            # We take the first one found
            app = apps[0]
            return app.processIdentifier()
        self._pid = get_pid_by_bundle_id(self.label)
        self._plist_fname = info.plist_path

    @property
    def plistfilename(self) -> str | None:
        """
        Lazily detect absolute filename of the property list file.

        Return None if it doesn't exist.
        """
        if self._plist_fname is None:
            self._plist_fname = discover_filename(self.label)
        return self._plist_fname


def jobs():
    for info in enumerate_services():
        job = LaunchdJob(info.label)
        job._properties = info.properties
        # job._pid = None
        job._plist_fname = info.plist_path
        yield job


def load(*args):
    return launchctl("load", *args)


def unload(*args):
    return launchctl("unload", *args)
