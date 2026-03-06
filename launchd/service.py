import os
import plistlib
from dataclasses import dataclass
from collections.abc import Iterator, Iterable

from Foundation import NSURL  # type: ignore[attr-defined]
import ServiceManagement

from .plist import PLIST_LOCATIONS


class ServiceStatus:
    ENABLED = getattr(ServiceManagement, "SMAppServiceStatusEnabled", 0)
    NOT_REGISTERED = getattr(ServiceManagement, "SMAppServiceStatusNotRegistered", 1)
    REQUIRES_APPROVAL = getattr(
        ServiceManagement, "SMAppServiceStatusRequiresApproval", 2
    )
    NOT_FOUND = getattr(ServiceManagement, "SMAppServiceStatusNotFound", 3)


_STATUS_NAMES = {
    ServiceStatus.ENABLED: "enabled",
    ServiceStatus.NOT_REGISTERED: "not_registered",
    ServiceStatus.REQUIRES_APPROVAL: "requires_approval",
    ServiceStatus.NOT_FOUND: "not_found",
}


def _status_to_name(status: int) -> str:
    return _STATUS_NAMES.get(status, "unknown")


def _expand_locations() -> dict[int, str]:
    result = {}
    for scope, location in PLIST_LOCATIONS.items():
        result[scope] = os.path.expanduser(location)
    return result


_SCOPE_DIRS = _expand_locations()


def _read_plist(path: str) -> dict | None:
    try:
        with open(path, "rb") as fh:
            return plistlib.load(fh)
    except Exception:
        return None


_SM_APP_SERVICE = getattr(ServiceManagement, "SMAppService", None)


def _status_for_path(path: str) -> int:
    if _SM_APP_SERVICE is None:
        return ServiceStatus.NOT_FOUND
    try:
        url = NSURL.fileURLWithPath_(path)
        status = _SM_APP_SERVICE.statusForLegacyURL_(url)
    except Exception:
        status = ServiceStatus.NOT_FOUND
    if status is None:
        return ServiceStatus.NOT_FOUND
    return int(status)


def _collect_plist_entries() -> Iterable[tuple[str, int, str]]:
    for scope in sorted(_SCOPE_DIRS):
        directory = _SCOPE_DIRS[scope]
        if not os.path.isdir(directory):
            continue
        try:
            entries = sorted(os.listdir(directory))
        except OSError:
            continue
        for entry in entries:
            if not entry.endswith(".plist"):
                continue
            label = entry[:-6]
            yield label, scope, os.path.join(directory, entry)


@dataclass(frozen=True)
class ServiceInfo:
    label: str
    plist_path: str
    scope: int
    status: int
    config: dict | None

    @property
    def status_name(self) -> str:
        return _status_to_name(self.status)

    @property
    def registered(self) -> bool:
        return self.status != ServiceStatus.NOT_REGISTERED

    @property
    def properties(self) -> dict:
        props = {
            "Label": self.label,
            "PlistPath": self.plist_path,
            "Scope": self.scope,
            "Status": self.status_name,
            "StatusCode": self.status,
            "Registered": self.registered,
        }
        if self.config is not None:
            for key, value in self.config.items():
                if key not in props:
                    props[key] = value
            props["Config"] = self.config
        return props


def enumerate_services() -> Iterator[ServiceInfo]:
    seen = set()
    for label, scope, path in _collect_plist_entries():
        if label.lower() in seen:
            continue
        seen.add(label.lower())
        # status = _status_for_path(path)
        status = None
        # config = _read_plist(path)
        config = None
        yield ServiceInfo(
            label=label,
            plist_path=path,
            scope=scope,
            status=status,
            config=config,
        )


def get_service_info(label: str) -> ServiceInfo | None:
    for info in enumerate_services():
        if info.label == label:
            return info
    return None
